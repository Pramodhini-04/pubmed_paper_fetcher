import requests
from typing import List, Tuple, Dict
from lxml import etree

ENTREZ_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ENTREZ_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

NON_ACADEMIC_KEYWORDS = [
    "inc", "llc", "ltd", "gmbh", "ag", "corp", "co.", "biotech", "pharma", "therapeutics",
    "Pfizer", "Novartis", "AstraZeneca", "GSK", "Merck", "Bayer", "Sanofi"
]

def search_pubmed(query: str, retmax: int = 50) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "xml",
        "retmax": retmax
    }
    response = requests.get(ENTREZ_SEARCH_URL, params=params)
    tree = etree.fromstring(response.content)
    return [id_elem.text for id_elem in tree.xpath("//IdList/Id")]

def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    ids = ",".join(pubmed_ids)
    params = {
        "db": "pubmed",
        "id": ids,
        "retmode": "xml"
    }
    response = requests.get(ENTREZ_FETCH_URL, params=params)
    tree = etree.fromstring(response.content)
    articles = []

    for article in tree.xpath("//PubmedArticle"):
        pubmed_id = article.xpath(".//PMID/text()")[0]
        title = article.xpath(".//ArticleTitle/text()")[0] if article.xpath(".//ArticleTitle/text()") else ""
        pub_date = "".join(article.xpath(".//PubDate/*/text()"))

        authors = []
        companies = []
        email = ""
        for author in article.xpath(".//Author"):
            affiliation = " ".join(author.xpath(".//AffiliationInfo/Affiliation/text()"))
            name = " ".join(author.xpath(".//LastName/text() | .//ForeName/text()"))
            if any(k.lower() in affiliation.lower() for k in NON_ACADEMIC_KEYWORDS):
                authors.append(name)
                companies.append(affiliation)
                if "@" in affiliation:
                    email = affiliation.split()[-1]

        articles.append({
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(set(authors)),
            "Company Affiliation(s)": "; ".join(set(companies)),
            "Corresponding Author Email": email
        })

    return articles