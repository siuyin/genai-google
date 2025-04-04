package main

import (
	"context"
	"fmt"
	"log"

	"github.com/siuyin/dflt"
	"google.golang.org/genai"
)

const model = "gemini-2.0-flash"

func main() {
	ctx := context.Background()
	key := dflt.EnvString("GEMINI_API_KEY", "your-key-here")
	log.Println("GEMINI_API_KEY=****")
	cl, err := genai.NewClient(ctx, &genai.ClientConfig{APIKey: key, Backend: genai.BackendGeminiAPI})
	if err != nil {
		log.Fatal(err)
	}

	fnCall(cl, "What is the weather like in Bukit Timah, Singapore?")
	fnCall(cl, "What is the weather like in Shewsberry, K2XPWD Glandon?")
	fnCall(cl, "What is the weather today?")
}

var (
	tools = []*genai.Tool{
		{FunctionDeclarations: []*genai.FunctionDeclaration{&weatherFuncDecl,&weatherPostcodeFuncDecl}},
	}

	weatherFuncDecl = genai.FunctionDeclaration{
		Name:        "weather",
		Description: "Get the current weather in a given location",
		Parameters: &genai.Schema{
			Type: genai.TypeObject,
			Properties: map[string]*genai.Schema{
				"location": {Type: genai.TypeString, Description: "The location eg. Bukit Timah, Singapore to get the weather for."},
			},
			Required: []string{"location"},
		},
	}
	weatherPostcodeFuncDecl = genai.FunctionDeclaration{
		Name:        "weatherPostcode",
		Description: "Get the current weather in a given location with postcode",
		Parameters: &genai.Schema{
			Type: genai.TypeObject,
			Properties: map[string]*genai.Schema{
				"location": {Type: genai.TypeString, Description: "The location eg. Bukit Timah, Singapore to get the weather for."},
				"postcode": {Type: genai.TypeString, Description: "postcode to get the weather for. eg1: Singapore 587967, eg2: XG6LK2 London"},
			},
			Required: []string{"location", "postcode"},
		},
	}
)

func fnCall(cl *genai.Client, prompt string) {
	fmt.Printf("Prompt: %s\n",prompt)

	ctx := context.Background()
	cfg := &genai.GenerateContentConfig{
		Tools: tools,
	}
	res, err := cl.Models.GenerateContent(ctx, model, genai.Text(prompt), cfg)
	if err != nil {
		log.Fatal(err)
	}

	for _, part := range res.Candidates[0].Content.Parts {
		if part.FunctionCall == nil {
			fmt.Printf("Text Response: %s\n", part.Text)
			break
		}
		p := part.FunctionCall
		// fmt.Printf("Function call request: name: %s, args: %v, id: %s\n", p.Name, p.Args, p.ID)
		switch p.Name {
		case "weather":
			fmt.Println(weather(p.Args["location"].(string)))
		case "weatherPostcode":
			fmt.Println(weatherPostcode(p.Args["location"].(string), p.Args["postcode"].(string)))
		default:
			log.Println("Unknown function call:", p.Name)
			break
		}
	}
	fmt.Println("----")
}

func weather(location string) string {
	return fmt.Sprintf("Weather in %s is sunny with a 40%% chance of rain\n", location)
}

func weatherPostcode(location string, postcode string) string {
	return fmt.Sprintf("Weather in %s with postcode %s is rainy with a 60%% chance of sun\n", location, postcode)
}
