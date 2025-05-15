## 🛠️ Setup

1.  **Prerequisites:** [Python X.X+ (or R X.X+)], [Conda (recommended) or pip/venv], [Git]
2.  **Clone:**
    ```bash
    git clone https://github.com/EYOELTEKLE/solar-challenge-week1
    cd solar-challenge-week1
    ```
3.  **Environment:**
    *   **Conda:**
        ```bash
        conda env create -f environment.yml
        conda activate [your_env_name]
        ```
    *   **pip & venv:**
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # Windows: .venv\Scripts\activate
        pip install -r requirements.txt
        ```
4.  **(Optional) Data:** [If data isn't in Git, explain how to get it and place it in `data/raw/`.]
5.  **Launch Jupyter/RStudio:**
    ```bash
    jupyter lab  # or jupyter notebook / RStudio
    ```

## 📓 Running Notebooks

1.  Activate your project environment.
2.  Launch your IDE (JupyterLab, RStudio).
3.  Open and run notebooks from the `notebooks/` directory, typically in numerical order. Outputs from earlier notebooks may be inputs for later ones.