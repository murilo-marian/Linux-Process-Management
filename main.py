import subprocess
import time
import psutil
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def get_process_count():
    command = "ps aux | wc -l"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return int(result.stdout.strip())

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    print(psutil.virtual_memory().used // 1000000)
    return psutil.virtual_memory().used // 1000000

def main():
    st.title("Contador de Processos")

    process_data = pd.DataFrame(columns=["Tempo", "Número de Processos"])
    cpu_data = pd.DataFrame(columns=["Tempo", "Uso da CPU (%)"])
    ram_data = pd.DataFrame(columns=["Tempo", "Uso da RAM"])


    chart_placeholder = st.empty()
    chart_placeholder_cpu = st.empty()
    chart_placeholder_ram = st.empty()

    while True:
        process_count = get_process_count()
        cpu_usage = get_cpu_usage()
        ram_usage = get_memory_usage()

        current_time = pd.Timestamp.now()

        new_data = pd.DataFrame({"Tempo": [current_time], "Número de Processos": [process_count]})
        process_data = pd.concat([process_data, new_data], ignore_index=True)
        
        new_cpu_data = pd.DataFrame({"Tempo": [current_time], "Uso da CPU (%)": [cpu_usage]})
        cpu_data = pd.concat([cpu_data, new_cpu_data], ignore_index=True)
        
        new_ram_data = pd.DataFrame({"Tempo": [current_time], "Uso da RAM": [ram_usage]})
        ram_data = pd.concat([ram_data, new_ram_data], ignore_index=True)

        plt.figure(figsize=(10, 5))
        plt.plot(process_data["Tempo"], process_data["Número de Processos"], marker='o')
        
        # Mudar escala e limites do gráfico
        min_y = process_data["Número de Processos"].min() - 10
        max_y = process_data["Número de Processos"].max() + 10
        plt.ylim(min_y, max_y)
        
        plt.xlabel("Tempo")
        plt.ylabel("Contagem de Processos")
        plt.title("Gráficos - Processos")
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_placeholder.pyplot(plt)
        
        plt.figure(figsize=(10, 5))
        plt.plot(cpu_data["Tempo"], cpu_data["Uso da CPU (%)"], marker='o', color='orange')
        plt.ylim(0, 100)
        plt.xlabel("Tempo")
        plt.ylabel("Uso da CPU (%)")
        plt.title("Gráfico - Uso da CPU")
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_placeholder_cpu.pyplot(plt)
        
        plt.figure(figsize=(10, 5))
        plt.plot(ram_data["Tempo"], ram_data["Uso da RAM"], marker='o', color='orange')
        min_y_ram = ram_data["Uso da RAM"].min() - 100
        max_y_ram = ram_data["Uso da RAM"].max() + 100
        plt.ylim(min_y_ram, max_y_ram)
        plt.xlabel("Tempo")
        plt.ylabel("Uso da RAM")
        plt.title("Gráfico - Uso da RAM")
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_placeholder_ram.pyplot(plt)
        
        time.sleep(10)

if __name__ == "__main__":
    main()