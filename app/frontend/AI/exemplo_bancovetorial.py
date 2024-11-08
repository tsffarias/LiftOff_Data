import chromadb
chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(name="expansao_liftoff")

collection.upsert(
    documents=[
        "A LiftOff vai abrir escritório no Brasil.",
        "A LiftOff vai abrir escritório na França.",
        "A LiftOff vai abrir escritório no Japão.",
        "A LiftOff vai abrir escritório na Alemanha.",
        "A LiftOff vai abrir escritório no Canadá.",
        "A LiftOff vai abrir escritório na Austrália.",
        "A LiftOff vai abrir escritório na Itália.",
        "A LiftOff vai abrir escritório na Argentina.",
        "A LiftOff vai abrir escritório na Espanha.",
        "A LiftOff vai abrir escritório na Rússia."
    ],
    ids=["pais1", "pais2", "pais3", "pais4", "pais5", "pais6", "pais7", "pais8", "pais9", "pais10"]
)

resultado = collection.query(
    query_texts=["O LiftOff terá um escritório no Rio de Janeiro?"],
    n_results=3
)

print(resultado)