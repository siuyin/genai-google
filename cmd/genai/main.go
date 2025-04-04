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

	// stream(cl, "How many planets are there in the Solar System? List them.")
	stream(cl, "Why is the sky blue?")

	// stream(cl, `Read the question below:
	// Prepare a response in the style of William Shakespeare.
	// Check your response and replace all old English term with modern equivalents,
	// then output your response.
	// Check that the modernized version has the same nuances as your original response.
	// If not prepare an improved response and repeat the process.

	// Also translate your final response to Chinese, providing both the chinese text and pinyin
	// for each line of output in json format as follows:
	// {[
	// {"english":"The meaning of this human experience",
	//  "chinese": "这人生意义的问题"
	//  "pinyin": "Zhè rénshēng yìyì de wèntí"},
	// {"english":"a question that bothers the minds of people",
	//  "chinese: "一个困扰人们的问题",
	//  "pinyin": "yī gè kùnrǎo rénmen de wèntí"}
	// ]}

	// Question:
	// What is the meaning of life?`)

}

func stream(cl *genai.Client, prompt string) {
	temp := float32(1.0)
	cfg := &genai.GenerateContentConfig{
		// SystemInstruction: &genai.Content{Parts: []*genai.Part{{Text: "Keep your responses brief and to the point."}}},
		Temperature:       &temp,
	}
	ctx := context.Background()
	for res, err := range cl.Models.GenerateContentStream(ctx, model, genai.Text(prompt), cfg) {
		if err != nil {
			log.Fatal(err)
		}
		fmt.Print(res.Candidates[0].Content.Parts[0].Text)
	}
	fmt.Println()
}
