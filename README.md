# 🧾 Générateur de factures PDF depuis Notion (Python)

Ce projet génère automatiquement des factures PDF à partir de données contenues dans deux bases de données Notion (Factures et Lignes de facture).

## 🔧 Configuration

1. Crée un fichier `.env` à la racine avec :

```
NOTION_API_KEY=secret_...
DATABASE_FACTURES_ID=...
DATABASE_LIGNES_ID=...
```

2. Installe les dépendances :

```
pip install -r requirements.txt
```

3. Lance le script :

```
python main.py
```

Les factures seront générées dans le dossier `factures/`.

## 📄 Structure Notion attendue

- Base **Factures** : Client, Adresse, Numéro de facture, Date, Total, Relation vers Lignes
- Base **Lignes de facture** : Article, Quantité, Prix unitaire, Total, Relation vers Facture
