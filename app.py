import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==========================================
# 1. LÓGICA DE NEGÓCIO (Geometria Automotiva)
# ==========================================
def calcular_medidas(largura_mm: int, perfil_pct: int, aro_pol: int) -> dict:
    """Calcula todas as cotas físicas do conjunto roda/pneu."""
    parede_mm = largura_mm * (perfil_pct / 100)
    aro_mm = aro_pol * 25.4
    total_mm = aro_mm + (2 * parede_mm)
    
    return {
        "parede_mm": parede_mm,
        "aro_mm": aro_mm,
        "total_mm": total_mm
    }

# ==========================================
# 2. MÓDULO VISUAL (Gráfico de Exibição)
# ==========================================
def gerar_grafico_showroom(medidas_orig, medidas_novo):
    # Fundo escuro/transparente com visual mais agressivo/moderno
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.patch.set_facecolor('none') 
    
    limite = max(medidas_orig["total_mm"], medidas_novo["total_mm"]) / 1.8 

    def desenhar(ax, medidas, titulo, cor_aro):
        # Pneu (Borracha)
        ax.add_patch(patches.Circle((0, 0), medidas["total_mm"] / 2, color='#1a1a1a', zorder=1))
        # Aro (Roda metálica)
        ax.add_patch(patches.Circle((0, 0), medidas["aro_mm"] / 2, color=cor_aro, zorder=2))
        
        ax.set_xlim(-limite, limite)
        ax.set_ylim(-limite, limite)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(titulo, fontsize=18, fontweight='bold', pad=20)
        
        # Linhas de cota visual
        raio_aro = medidas["aro_mm"] / 2
        raio_total = medidas["total_mm"] / 2
        
        # Texto do Perfil no meio da borracha
        meio_borracha = raio_aro + ((raio_total - raio_aro) / 2)
        ax.text(0, meio_borracha, f"Perfil:\n{medidas['parede_mm']:.1f} mm", 
                ha='center', va='center', color='white', fontsize=10, fontweight='bold')

    desenhar(ax1, medidas_orig, "Setup Original", "#737373")  # Roda original prata/cinza
    desenhar(ax2, medidas_novo, "Novo Projeto", "#b8860b")   # Roda de projeto dourada/bronze para destaque
    
    plt.tight_layout()
    return fig

# ==========================================
# 3. INTERFACE DO USUÁRIO (Modo Notebook/Feira)
# ==========================================
def main():
    # Configuração de tela mais larga para aproveitar o notebook
    st.set_page_config(page_title="Geometria de Rodas", layout="wide")
    
    st.markdown("<h1 style='text-align: center;'>📏 Calculadora de Altura e Fitment</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Simule o impacto do novo setup na altura do chassi.</p>", unsafe_allow_html=True)
    st.write("")

    # Área de Inputs (Compacta e lado a lado)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Setup Original")
        c1, c2, c3 = st.columns(3)
        larg_orig = c1.number_input("Largura (mm)", value=205, step=5, key="l1")
        perf_orig = c2.number_input("Perfil (%)", value=55, step=5, key="p1")
        aro_orig = c3.number_input("Aro (pol)", value=16, step=1, key="a1")

    with col2:
        st.subheader("🔥 Novo Projeto")
        c4, c5, c6 = st.columns(3)
        larg_novo = c4.number_input("Largura (mm)", value=225, step=5, key="l2")
        perf_novo = c5.number_input("Perfil (%)", value=45, step=5, key="p2")
        aro_novo = c6.number_input("Aro (pol)", value=18, step=1, key="a2")

    # Extraindo as medidas
    medidas_orig = calcular_medidas(larg_orig, perf_orig, aro_orig)
    medidas_novo = calcular_medidas(larg_novo, perf_novo, aro_novo)
    
    # A diferença de altura do chassi em relação ao solo é o raio (metade do diâmetro) dividido por 10 (para cm)
    dif_altura_cm = ((medidas_novo["total_mm"] - medidas_orig["total_mm"]) / 2) / 10

    st.divider()

    # O "Painel" de Resultados (Onde o cliente da feira vai olhar)
    res1, res2, res3 = st.columns(3)
    
    res1.metric("Diâmetro Total Original", f"{medidas_orig['total_mm'] / 10:.1f} cm")
    res2.metric("Diâmetro Total do Projeto", f"{medidas_novo['total_mm'] / 10:.1f} cm", delta=f"{(medidas_novo['total_mm'] - medidas_orig['total_mm']) / 10:.1f} cm no espaço da caixa de roda")
    
    # A métrica principal do app: A Altura do Carro
    if dif_altura_cm > 0:
        texto_altura = "Mais ALTO em relação ao solo ⬆️"
        cor_delta = "normal"
    elif dif_altura_cm < 0:
        texto_altura = "Mais BAIXO em relação ao solo ⬇️"
        cor_delta = "inverse"
    else:
        texto_altura = "Mesma altura do solo ↔️"
        cor_delta = "off"

    res3.metric("Impacto na Altura do Carro", f"{abs(dif_altura_cm):.1f} cm", delta=texto_altura, delta_color=cor_delta)

    st.divider()
    
    # Gráfico renderizado bem grande na parte inferior
    figura = gerar_grafico_showroom(medidas_orig, medidas_novo)
    st.pyplot(figura, use_container_width=True)

if __name__ == "__main__":
    main()