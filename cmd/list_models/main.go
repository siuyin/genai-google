package main

import (
	"context"
	"fmt"
	"log"

	"github.com/siuyin/dflt"
	"google.golang.org/genai"
)

func main() {
	ctx := context.Background()
	key := dflt.EnvString("GEMINI_API_KEY", "your-key-here")
	log.Println("GEMINI_API_KEY=****")
	cl, err := genai.NewClient(ctx, &genai.ClientConfig{APIKey: key, Backend: genai.BackendGeminiAPI})
	if err != nil {
		log.Fatal(err)
	}

	for m,err:=range cl.Models.All(ctx){
		if err!=nil{
			log.Fatal(err)
		}
		prettyPrint(m)
	}
}

func prettyPrint(m *genai.Model) {
	fmt.Printf("%s: %s\n", m.Name, m.Description)
}

