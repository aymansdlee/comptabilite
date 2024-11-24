package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {

	// Open the shipping prices file
	pricesFile, err := os.Open("shipping_prices.csv")
	if err != nil {
		fmt.Printf("Error opening shipping prices file: %v\n", err)
		return
	}
	defer pricesFile.Close()

	// Read the shipping prices file into a map
	pricesReader := csv.NewReader(pricesFile)
	priceHeaders, err := pricesReader.Read() // Read the header row
	if err != nil {
		fmt.Printf("Error reading shipping prices headers: %v\n", err)
		return
	}

	// Parse the items and prices into a nested map: item -> country -> price
	prices := make(map[string]map[string]float64)
	for {
		record, err := pricesReader.Read()
		if err != nil {
			break // EOF or error
		}

		item := strings.TrimSpace(record[0])
		prices[item] = make(map[string]float64)

		for i, priceStr := range record[1:] {
			country := strings.TrimSpace(priceHeaders[i+1])
			if priceStr == "" || country == "" {
				continue
			}
			price, err := strconv.ParseFloat(priceStr, 64)
			if err != nil {
				fmt.Printf("Error parsing price for item %s, country %s: %v\n", item, country, err)
				continue
			}
			prices[item][country] = price
		}
	}

	// Open the order file
	file, err := os.Open("ordersexport.csv")
	if err != nil {
		fmt.Printf("Error opening orders file: %v\n", err)
		return
	}
	defer file.Close()

	// Create a CSV reader
	reader := csv.NewReader(file)

	// Read the header row
	headers, err := reader.Read()
	if err != nil {
		fmt.Printf("Error reading header row: %v\n", err)
		return
	}

	// Find the indices of the required columns
	nameIndex := -1
	itemIndex := -1
	countryIndex := -1
	quantityIndex := -1
	for i, header := range headers {
		switch header {
		case "Name":
			nameIndex = i
		case "Lineitem name":
			itemIndex = i
		case "Shipping Country":
			countryIndex = i
		case "Lineitem quantity":
			quantityIndex = i
		}
	}

	// Check if the required columns exist
	if nameIndex == -1 || itemIndex == -1 || countryIndex == -1 || quantityIndex == -1 {
		fmt.Println("One or more required columns not found.")
		return
	}

	// Process each order row
	fmt.Println("Filtered Orders:")
	var currentName string
	var lastCountry string

	// Track the number of orders with both suitcases in the same name
	countSuitcasesInSameOrder := 0

	// Track the presence of suitcases per customer
	customerSuitcases := make(map[string]map[string]bool)

	// Process orders
	for {
		record, err := reader.Read()
		if err != nil {
			break // EOF or error
		}

		// Extract the name, item, country, and quantity
		name := record[nameIndex]
		item := strings.TrimSpace(record[itemIndex])
		country := strings.TrimSpace(record[countryIndex])
		quantityStr := record[quantityIndex]

		// Update the last valid country for the current customer
		if country != "" {
			lastCountry = country
		}

		// Convert quantity to an integer
		quantity, err := strconv.Atoi(quantityStr)
		if err != nil {
			fmt.Printf("Error converting quantity to integer for item: %s. Skipping.\n", item)
			continue
		}

		// Remove color and slashes from the item name
		cleanedItem := strings.ReplaceAll(item, "/ Black", "")
		cleanedItem = strings.ReplaceAll(cleanedItem, "/ Silver", "")
		cleanedItem = strings.ReplaceAll(cleanedItem, "/", "")
		cleanedItem = strings.TrimSpace(cleanedItem) // Ensure no trailing spaces

		// Skip the item if it's not in the prices map
		if _, ok := prices[cleanedItem]; !ok {
			continue
		}

		// Print the item details
		if name != currentName {
			if currentName != "" {
				// Print the count of orders with both suitcases for the previous customer
				if customerSuitcases[currentName]["Large"] && customerSuitcases[currentName]["Carry-on"] {
					countSuitcasesInSameOrder++
				}

				// Reset the suitcases tracking after printing
				customerSuitcases[currentName] = make(map[string]bool)
			}
			fmt.Println() // Add a blank line between different names
			fmt.Printf("Name: %s\n", name)
			currentName = name
		}
		fmt.Printf("  Item: %s, Country: %s, Quantity: %d, Price: %.2f\n", cleanedItem, lastCountry, quantity, prices[cleanedItem][lastCountry])

		// Track the suitcases for the current order
		isLargeSuitcase := cleanedItem == "Nomad Aluminium Suitcase - Large"
		isCarryOnSuitcase := cleanedItem == "Nomad Aluminium Suitcase - Carry-on"

		// Add the suitcases to the customer's record
		if _, exists := customerSuitcases[name]; !exists {
			customerSuitcases[name] = make(map[string]bool)
		}
		if isLargeSuitcase {
			customerSuitcases[name]["Large"] = true
		}
		if isCarryOnSuitcase {
			customerSuitcases[name]["Carry-on"] = true
		}
	}

	// Check and print the last customer
	if customerSuitcases[currentName]["Large"] && customerSuitcases[currentName]["Carry-on"] {
		countSuitcasesInSameOrder++
	}

	// Print the count of orders where both suitcases appear for the same customer
	fmt.Printf("\nTotal orders with both suitcases for the same customer: %d\n", countSuitcasesInSameOrder)
}
