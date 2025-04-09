from cog.torque import Graph


def main():
    g = open_db()
    g = load_triples(g)
    print("_picnic1 details:")
    connections(g, "_picnic1")
    print("\n_picnic1 attendees:")
    converge(g, "_picnic1")


def open_db() -> any:
    return Graph("Flintstones", cog_home="db", cog_path_prefix="./")


def load_triples(g: any) -> any:
    g.load_triples("testdata/flintstones.nt")
    return g


def converge(g, n: str):
    r = g.v(n).inc().all()
    for p in r["result"]:
        print(p["id"])


def connections(g, n: str) -> None:
    r = g.v(n).out().all("e")
    for p in r["result"]:
        print(f"""{p["edges"]}: {p["id"]}""")


if __name__ == "__main__":
    main()
