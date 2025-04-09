import ollama as o

def main():
    m=o.list().models[0].model
    print(m)
    print(o.show(m).details)

if __name__ == "__main__":
    main()