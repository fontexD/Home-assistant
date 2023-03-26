package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"regexp"
	"time"

	"github.com/eclipse/paho.mqtt.golang"
)

type Delta struct {
	Values map[string]int `json:"values"`
}

func main() {
	// Define the URL to scrape
	url := "<scrape url>"

	// Define the MQTT broker address, username, and password
	brokerAddress := "tcp://192.168.1.58:1883"
	username := "MQTT"
	password := "<redacted>"

	// Create an MQTT client options object with the specified credentials
	opts := mqtt.NewClientOptions()
	opts.AddBroker(brokerAddress)
	opts.SetUsername(username)
	opts.SetPassword(password)

	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}

	re := regexp.MustCompile(`Actual Power \[W\]\s*<\/td>\s*<td[^>]*>\s*([\d.]+)`)
	re2 := regexp.MustCompile(`Total Energy \[kWh\]\s*<\/td>\s*<td[^>]*>\s*([\d.]+)`)

	// Loop indefinitely
	for {
		response, err := http.Get(url)
		if err != nil {
			panic(err)
		}

		defer response.Body.Close()

		body, err := ioutil.ReadAll(response.Body)
		if err != nil {
			panic(err)
		}

		html := string(body)

		match := re.FindStringSubmatch(html)
		if len(match) != 2 {
			panic("Could not find Actual Power [W]")
		}

		match2 := re2.FindStringSubmatch(html)
		if len(match2) != 2 {
			panic("Could not find Actual Total [kWH]")
		}
		value := match[1]
		value2 := match2[1]

		delta := Delta{
			Values: map[string]int{
				"pv1watt": atoi(value),
				"total":   atoi(value2),
			},
		}

		jsonData, err := json.Marshal(delta)
		if err != nil {
			panic(err)
		}

		topic := "delta"
		token := client.Publish(topic, 0, false, jsonData)
		token.Wait()

		fmt.Printf("Published %s to topic %s\n", jsonData, topic)

		time.Sleep(10 * time.Second)
	}
}

// atoi converts a string to an integer
func atoi(s string) int {
	n := 0
	for _, ch := range s {
		n = n*10 + int(ch-'0')
	}
	return n
}
