from cog.torque import Graph


def main():
    g = Graph("Flintstones", cog_home="db", cog_path_prefix="./")
    g.put("_alice", "name", "alice")
    g.put("_alice", "sex", "female")
    g.put("_bob", "name", "bob")
    g.put("_bob", "sex", "male")
    g.put("_bob", "follows", "_alice")
    g.put("_bib", "name", "bob")
    # print(g.v("_bob").out().all("e"))
    # print(g.v().all())
    # print(g.v("bob").inc("name").all())
    # which_ids_are_named(g, "bob")
    connections(g,"_bob")

def connections(g, n:str)->None:
    r= g.v(n).out().all("e")
    for p in r["result"]:
        print(f"""{p["edges"]}: {p["id"]}""")

def which_ids_are_named(g: any, n: str) -> None:
    r = g.v(n).inc("name").all()
    for p in r["result"]:
        print(p["id"])


if __name__ == "__main__":
    main()
