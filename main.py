import os
from notion_client import Client
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

load_dotenv()
notion = Client(auth=os.getenv("NOTION_API_KEY"))

FACTURES_DB = os.getenv("DATABASE_FACTURES_ID")
LIGNES_DB = os.getenv("DATABASE_LIGNES_ID")

def get_lignes_facture(facture_id):
    lignes = []
    results = notion.databases.query(
        **{
            "database_id": LIGNES_DB,
            "filter": {
                "property": "Facture",
                "relation": {
                    "contains": facture_id
                }
            }
        }
    )["results"]

    for ligne in results:
        props = ligne["properties"]
        lignes.append({
            "article": props["Article"]["title"][0]["text"]["content"],
            "qte": props["Quantité"]["number"],
            "pu": props["Prix unitaire"]["number"],
            "total": props["Total"]["number"]
        })
    return lignes

def generate_facture(facture):
    props = facture["properties"]
    id_facture = facture["id"]

    contexte = {
        "client": props["Client"]["rich_text"][0]["text"]["content"],
        "adresse": props["Adresse"]["rich_text"][0]["text"]["content"],
        "date": props["Date"]["date"]["start"],
        "numero_facture": props["Numéro de facture"]["rich_text"][0]["text"]["content"],
        "total": props["Total"]["number"],
        "lignes": get_lignes_facture(id_facture)
    }

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("facture.html")
    html_out = template.render(**contexte)

    os.makedirs("factures", exist_ok=True)
    filename = f"factures/facture_{contexte['numero_facture']}.pdf"
    HTML(string=html_out).write_pdf(filename)
    print(f"✅ Facture générée : {filename}")

def main():
    results = notion.databases.query(database_id=FACTURES_DB)["results"]
    for facture in results:
        generate_facture(facture)

if __name__ == "__main__":
    main()
