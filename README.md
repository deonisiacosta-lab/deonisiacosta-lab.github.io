# Aplikasaun Segmentasaun Kliente uza K-Means no PCA

Aplikasaun web interativu no pipeline machine learning ne'ebé dezenvolve hodi halo segmentasaun ba kliente mall nian bazeia ba rendimentu annual no puntu gastu, hodi uza **Unsupervised Learning (K-Means Clustering)** no **Principal Component Analysis (PCA)**.

---

## 🚀 Funsaun Xave
- **Dashboard Interativu:** Kria ho **Streamlit** hodi esplora no vizualiza dadus kliente iha tempu reál.
- **K-Means Clustering Automatizadu:** Agrupa kliente ba kategoria haat ($K=4$) ne'ebé determina hodi uza Metodu Elbow no valida ho Silhouette Score ($0.4164$).
- **Redusaun Dimensaun (PCA):** Transforma dadus kompleksu sai ba espasu koordenada 2D hodi vizualiza iha grafiku *scatter plot*.
- **Prediksaun Kliente Foun:** Permiti utente hatama dadus kliente foun (Jéneru, Idade, Rendimentu Anual, Puntu Gastu) hodi hatene kedas nia kategoria cluster.
- **Análize Korelasaun:** Matriz korelasaun Pearson interativu hodi komprende relasaun entre váriavel sira.

---

## 📊 Sumáriu Kategoria Kliente
| Cluster | Naran Kategoria | Karakterístika | Estratéjia Marketing |
| :--- | :--- | :--- | :--- |
| **Cluster 1** | **Kliente VIP** | Rendimentu Aas, Puntu Gastu Aas | Tratamentu eskluzivu, programa lealdade (*loyalty program*), no promosaun produtu premium. |
| **Cluster 2** | **Kliente Standar** | Rendimentu Normal, Puntu Gastu Moderadu | Baze sólidu ba transasaun diáriu no estabilidade rendimentu empreza. |
| **Cluster 3** | **Kliente Joven** | Rendimentu Ki'ik, Puntu Gastu Aas | Kampanha marketing dijital ne'ebé flexible, trend, no desconto atrai. |
| **Cluster 4** | **Kliente Potensial** | Rendimentu Moderadu, Puntu Gastu Moderadu | Kampanha hodi sa'e sira ba kategoria VIP. |

---

## 🛠️ Teknolojia no Biblioteka (Tech Stack)
- **Python** (Lian programasaun prinsipál)
- **Streamlit** (Framework web ba UI)
- **Scikit-Learn** (Modelu Machine Learning: K-Means, PCA, StandardScaler)
- **Pandas & NumPy** (Manipulasaun dadus)
- **Matplotlib & Seaborn** (Vizualizasaun dadus)

---

## ⚙️ Oinsá Husu / Halo Run iha Komputador Rasik (Run Locally)

1. **Clone repositóriu ne'e:**
   ```bash
   git clone [https://github.com/deonisiacosta-lab/deonisiacosta-lab.github.io.git](https://github.com/deonisiacosta-lab/deonisiacosta-lab.github.io.git)
   cd deonisiacosta-lab.github.io
