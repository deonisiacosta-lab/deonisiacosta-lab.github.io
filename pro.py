import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Aplikasaun Segmentasaun Kliente (K-Means + PCA)", layout="wide"
)

# 1. Upload Dataset
st.header("Upload Dataset Marketing")
uploaded_file = st.file_uploader("Hili file CSV", type=["csv"])

if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  df = df.drop_duplicates().reset_index(drop=True)

  # --- ENCODING GENDER / GENRE ---
  gender_col = None
  if "Gender" in df.columns:
    gender_col = "Gender"
  elif "Genre" in df.columns:
    gender_col = "Genre"

  if gender_col:
    df["Gender_Numeric"] = df[gender_col].map({"Female": 0, "Male": 1})

  raw_numeric = df.select_dtypes(include=[np.number]).columns.tolist()

  for col in [
      "CustomerID",
      "customer_id",
      "Customer_ID",
      "order_id",
      "user_id",
      "ID",
      "id",
  ]:
    if col in raw_numeric:
      raw_numeric.remove(col)

  numeric_cols = []
  if "Gender_Numeric" in raw_numeric:
    numeric_cols.append("Gender_Numeric")
    raw_numeric.remove("Gender_Numeric")

  numeric_cols.extend(raw_numeric)
  selected_features = numeric_cols

  if len(selected_features) < 2:
    st.warning("Favor ida uza dataset ne'ebé iha pelo menus columna numeriku 2.")
  else:
    X = df[selected_features]
    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X)
    X_imputed_df = pd.DataFrame(X_imputed, columns=selected_features)

    # StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed_df)

    # PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    df_pca = pd.DataFrame(X_pca, columns=["PC1", "PC2"])

    # --- SIDEBAR: KONTROLU TOTAL CLUSTER (K) DINAMIKU ---
    st.sidebar.title("Dokumentasaun Modelu")
    chosen_k = st.sidebar.slider(
        "Hili Total Cluster (K):", min_value=2, max_value=4, value=3
    )
    st.sidebar.markdown(f"""
    - **Modelu:** Customer Segmentation no PCA
    - **Algoritmu:** K-Means Clustering
    - **Metodu:** Unsupervised Learning
    """)

    # Title
    st.title("Aplikasaun Segmentasaun Kliente (K-Means + PCA)")

    # K-MEANS HO CHOSEN_K HUSI SLIDER ATU HARE MUDANSA SILHOUETTE SCORE
    kmeans = KMeans(n_clusters=chosen_k, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_pca)

    df["Cluster"] = cluster_labels
    df_pca["Cluster"] = cluster_labels

    # Kalkula fali Silhouette Score ho dinamiku tuir chosen_k
    current_score = silhouette_score(X_pca, cluster_labels)

    # --- RAI MODELU HO PICKLE ---
    with open("kmeans_model.pkl", "wb") as f:
      pickle.dump(kmeans, f)
    with open("scaler_model.pkl", "wb") as f:
      pickle.dump(scaler, f)
    with open("pca_model.pkl", "wb") as f:
      pickle.dump(pca, f)

    # --- MAPEAMENTU NARAN SEGMENTU BAZAIA BA TOTAL K ---
    if chosen_k == 2:
      base_cluster_mapping = {0: "Kliente VIP", 1: "Kliente Standar"}
    elif chosen_k == 3:
      # Bainhira K = 3, uza de'it VIP, Standar no Potensial
      base_cluster_mapping = {
          0: "Kliente VIP",
          1: "Kliente Standar",
          2: "Kliente Potensial",
      }
    else:  # K = 4
      base_cluster_mapping = {
          0: "Kliente VIP",
          1: "Kliente Standar",
          2: "Kliente Joven",
          3: "Kliente Potensial",
      }

    cluster_mapping = {}
    for i in range(chosen_k):
      cluster_mapping[i] = base_cluster_mapping.get(i, f"Kliente {i+1}")

    df["Segmento"] = df["Cluster"].map(cluster_mapping)
    df_pca["Segmento"] = df_pca["Cluster"].map(cluster_mapping)
    segment_options = list(cluster_mapping.values())

    # --- MENU HORIZONTAL IHA LETEN ---
    st.markdown("---")
    menu = st.radio(
        "Hili Menu Navigasaun:",
        [
            "Dashboard & Prediksaun",
            "Matriz Korelasaun Detail",
            "Tabela Dadus Kliente",
        ],
        horizontal=True,
    )
    st.markdown("---")

    # --- KONTROLU MENU ---
    if menu == "Dashboard & Prediksaun":
      st.subheader("Dadus Kliente (Orijinál):")
      st.dataframe(df.head())

      # 3. Filtru Segmentu
      st.header("Filtru Segmentu Kliente")
      selected_segment = st.multiselect(
          "Hili segmentu ne'ebé atu hatudu de'it:",
          options=segment_options,
          default=segment_options,
      )
      df_filtered = df[df["Segmento"].isin(selected_segment)]
      df_pca_filtered = df_pca[df_pca["Segmento"].isin(selected_segment)]

      # 4. Input no Prevé Kliente Foun
      st.header("Input no Prevé Kliente Foun")
      input_data = []
      cols = st.columns(len(selected_features))

      for idx, feature_name in enumerate(selected_features):
        with cols[idx]:
          if feature_name == "Gender_Numeric":
            gender_select = st.selectbox(
                "Jéneru (Gender):", options=["Female", "Male"]
            )
            val = 0 if gender_select == "Female" else 1
          else:
            default_val = float(X_imputed_df[feature_name].median())
            val = st.number_input(f"{feature_name}:", value=default_val)
          input_data.append(val)

      new_data = np.array([input_data])
      new_data_scaled = scaler.transform(new_data)
      new_data_pca = pca.transform(new_data_scaled)

      pred_cluster = kmeans.predict(new_data_pca)[0]
      pred_segment = cluster_mapping[pred_cluster]

      st.success(
          f"*Rezultadu Prediksaun K-Means (PCA):* Kliente foun ne'e tama ba"
          f" **{pred_segment}**"
      )

      # 5. Gráfiku Segmentasaun PCA
      st.header("Gráfiku Segmentasaun Kliente (PCA Dimension)")
      fig, ax = plt.subplots(figsize=(10, 6))

      colors = [
          "#ff4b4b",
          "#0068c9",
          "#33cc33",
          "#ffaa00",
          "#9933ff",
          "#ff3399",
      ]
      for idx_seg, (segment, group) in enumerate(
          df_pca_filtered.groupby("Segmento")
      ):
        ax.scatter(
            group["PC1"],
            group["PC2"],
            label=segment,
            color=colors[idx_seg % len(colors)],
            alpha=0.7,
            s=50,
        )

      ax.scatter(
          new_data_pca[0, 0],
          new_data_pca[0, 1],
          color="black",
          edgecolors="white",
          marker="*",
          s=300,
          label="Kliente Foun",
      )

      var_pc1 = pca.explained_variance_ratio_[0] * 100
      var_pc2 = pca.explained_variance_ratio_[1] * 100

      ax.set_xlabel(f"Principal Component 1 ({var_pc1:.1f}% Variance)")
      ax.set_ylabel(f"Principal Component 2 ({var_pc2:.1f}% Variance)")
      ax.set_title(
          f"Visualizasaun Cluster K={chosen_k} iha Dimensaun PCA Jenerál"
      )
      ax.legend(loc="upper right")
      ax.grid(True, linestyle="--", alpha=0.5)
      st.pyplot(fig)

      # 7. Kualidade Fahe Cluster (Silhoute Score Troka Tuir K)
      st.header("Kualidade Fahe Cluster (PCA Space)")
      st.metric(
          label=f"Silhouette Score (Model K={chosen_k})",
          value=f"{current_score:.4f}",
      )
      st.info(
          "Kualidade agrupamentu modelu nian troka ho dinamiku bazeia ba"
          " numero cluster (K) ne'ebé Ita hili iha sidebar."
      )

    elif menu == "Matriz Korelasaun Detail":
      st.header("Matriz Korelasaun Feature ho Segmentu Kliente Hotu")

      df_corr_cluster = X_imputed_df.copy()
      for cluster_id, seg_name in cluster_mapping.items():
        df_corr_cluster[seg_name] = (df["Cluster"] == cluster_id).astype(int)

      corr_matrix_all = df_corr_cluster.corr()

      fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
      sns.heatmap(
          corr_matrix_all,
          annot=True,
          cmap="coolwarm",
          vmin=-1,
          vmax=1,
          fmt=".2f",
          linewidths=0.5,
          ax=ax_corr,
      )
      ax_corr.set_xticklabels(
          ax_corr.get_xticklabels(), rotation=45, ha="right"
      )
      st.pyplot(fig_corr)

      st.info(
          "Matriz ida ne'e hatudu relasaun direta inter-feature no mós ho"
          " segmentu kliente sira."
      )

    elif menu == "Tabela Dadus Kliente":
      st.header("Tabela Dadus Cluster Kompletu:")
      st.dataframe(df)

      csv = df.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="Download Dadus Cluster (CSV)",
          data=csv,
          file_name="segmented_customers_complete.csv",
          mime="text/csv",
      )

else:
  st.info("Favor ida upload file CSV atu hahú aplikasaun.")