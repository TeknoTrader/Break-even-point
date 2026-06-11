# -*- coding: utf-8 -*-
# Dashboard break-even per la vendita B2C di pizza tramite distributori automatici.
# App Streamlit bilingue (IT / UK), predisposta per deploy su Streamlit Community Cloud via GitHub.

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="PIZZA 24 - Break-Even B2C", layout="wide")

# Dizionario di traduzione: chiave -> {it, uk}
I18N = {
    "app_title": {"it": "Break-Even B2C - Distributori di Pizza", "uk": "Беззбитковість B2C - Піца-автомати"},
    "app_sub": {"it": "Modello finanziario per la vendita diretta al consumatore.",
                "uk": "Фінансова модель прямого продажу споживачу."},
    "lang_label": {"it": "Lingua", "uk": "Мова"},

    "h_invest": {"it": "Investimento", "uk": "Інвестиції"},
    "capex": {"it": "CAPEX per distributore (EUR)", "uk": "CAPEX на автомат (EUR)"},
    "machines": {"it": "Numero di distributori", "uk": "Кількість автоматів"},

    "h_revenue": {"it": "Ricavi", "uk": "Доходи"},
    "price": {"it": "Prezzo medio pizza (EUR)", "uk": "Середня ціна піци (EUR)"},
    "ppd": {"it": "Pizze al giorno (per distributore)", "uk": "Піц на день (на автомат)"},
    "foodcost": {"it": "Food cost (%)", "uk": "Собівартість продукту (%)"},

    "h_opex": {"it": "Costi mensili fissi (per distributore)", "uk": "Постійні витрати на місяць (на автомат)"},
    "rent": {"it": "Affitto postazione (EUR)", "uk": "Оренда місця (EUR)"},
    "power": {"it": "Energia elettrica (EUR)", "uk": "Електроенергія (EUR)"},
    "conn": {"it": "Connettivita e fiscalizzazione (EUR)", "uk": "Звязок та фіскалізація (EUR)"},
    "maint": {"it": "Manutenzione e consumabili (EUR)", "uk": "Обслуговування та витратні (EUR)"},
    "staff_cost": {"it": "Costo mensile addetto HACCP (EUR)", "uk": "Зарплата працівника HACCP / міс (EUR)"},
    "staff_ratio": {"it": "Distributori per addetto", "uk": "Автоматів на одного працівника"},

    "h_tax": {"it": "Fiscalita", "uk": "Оподаткування"},
    "tax": {"it": "Aliquota IRES+IRAP (%)", "uk": "Ставка IRES+IRAP (%)"},
    "amort": {"it": "Orizzonte ammortamento CAPEX (mesi)", "uk": "Горизонт амортизації CAPEX (міс)"},

    "kpi_title": {"it": "Risultati per distributore", "uk": "Результати на один автомат"},
    "k_gross": {"it": "Margine lordo / mese", "uk": "Валовий прибуток / міс"},
    "k_net": {"it": "Utile netto / mese", "uk": "Чистий прибуток / міс"},
    "k_bep_opex": {"it": "Pareggio OPEX (pizze/giorno)", "uk": "Беззбитковість OPEX (піц/день)"},
    "k_bep_full": {"it": "Pareggio con CAPEX (pizze/giorno)", "uk": "Беззбитковість з CAPEX (піц/день)"},
    "k_payback": {"it": "Rientro investimento", "uk": "Окупність"},
    "months": {"it": "mesi", "uk": "міс"},
    "na": {"it": "n/d", "uk": "н/д"},

    "net_title": {"it": "Utile netto in funzione delle vendite", "uk": "Чистий прибуток залежно від продажів"},
    "net_x": {"it": "Pizze al giorno", "uk": "Піц на день"},
    "net_y": {"it": "Utile netto / mese (EUR)", "uk": "Чистий прибуток / міс (EUR)"},
    "net_line": {"it": "Utile netto", "uk": "Чистий прибуток"},
    "bep_marker": {"it": "Punto di pareggio", "uk": "Точка беззбитковості"},

    "cf_title": {"it": "Flusso di cassa cumulato (rete)", "uk": "Накопичений грошовий потік (мережа)"},
    "cf_x": {"it": "Mesi", "uk": "Місяці"},
    "cf_y": {"it": "Cassa cumulata (EUR)", "uk": "Накопичена каса (EUR)"},
    "cf_line": {"it": "Cassa cumulata", "uk": "Накопичена каса"},
    "cf_bep": {"it": "Rientro", "uk": "Окупність"},

    "scen_title": {"it": "Analisi per scenari (per distributore)", "uk": "Аналіз за сценаріями (на автомат)"},
    "scen_name": {"it": "Scenario", "uk": "Сценарій"},
    "scen_low": {"it": "Pessimistico", "uk": "Песимістичний"},
    "scen_base": {"it": "Base", "uk": "Базовий"},
    "scen_high": {"it": "Ottimistico", "uk": "Оптимістичний"},
    "scen_ppd": {"it": "Pizze/giorno", "uk": "Піц/день"},
    "scen_rev": {"it": "Ricavi/mese", "uk": "Дохід/міс"},
    "scen_net": {"it": "Utile netto/mese", "uk": "Чистий прибуток/міс"},
    "scen_pay": {"it": "Rientro (mesi)", "uk": "Окупність (міс)"},

    "net_note": {"it": "Stima al netto di IRES+IRAP. Le imposte si applicano solo all'utile positivo. "
                       "Verificare le aliquote con un commercialista.",
                 "uk": "Оцінка з урахуванням IRES+IRAP. Податки застосовуються лише до позитивного прибутку. "
                       "Уточніть ставки у бухгалтера."},
    "network_note": {"it": "Valori di rete = valori per distributore moltiplicati per il numero di distributori.",
                     "uk": "Показники мережі = показники на автомат, помножені на кількість автоматів."},
}


def t(key, lang):
    return I18N[key][lang]


def fmt(value, lang, dec=0):
    # Formattazione numerica con separatore migliaia e decimale per locale
    s = f"{value:,.{dec}f}"  # formato base: 1,234.56
    if lang == "it":
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    else:  # uk: spazio per le migliaia, virgola decimale
        s = s.replace(",", " ").replace(".", ",")
    return s


# Selettore lingua
lang = st.sidebar.radio(I18N["lang_label"]["it"] + " / " + I18N["lang_label"]["uk"],
                        options=["it", "uk"],
                        format_func=lambda x: "Italiano" if x == "it" else "Українська")

st.title(t("app_title", lang))
st.caption(t("app_sub", lang))

# --- INPUT (sidebar) ---
st.sidebar.header(t("h_invest", lang))
capex = st.sidebar.number_input(t("capex", lang), min_value=0, value=10000, step=500)
n_machines = st.sidebar.number_input(t("machines", lang), min_value=1, value=1, step=1)

st.sidebar.header(t("h_revenue", lang))
price = st.sidebar.number_input(t("price", lang), min_value=0.0, value=7.0, step=0.1)
ppd = st.sidebar.slider(t("ppd", lang), min_value=0, max_value=120, value=30, step=1)
foodcost = st.sidebar.slider(t("foodcost", lang), min_value=0, max_value=100, value=22, step=1)

st.sidebar.header(t("h_opex", lang))
rent = st.sidebar.number_input(t("rent", lang), min_value=0, value=300, step=50)
power = st.sidebar.number_input(t("power", lang), min_value=0, value=150, step=10)
conn = st.sidebar.number_input(t("conn", lang), min_value=0, value=50, step=10)
maint = st.sidebar.number_input(t("maint", lang), min_value=0, value=200, step=10)
staff_cost = st.sidebar.number_input(t("staff_cost", lang), min_value=0, value=2000, step=100)
staff_ratio = st.sidebar.number_input(t("staff_ratio", lang), min_value=1, value=5, step=1)

st.sidebar.header(t("h_tax", lang))
tax = st.sidebar.slider(t("tax", lang), min_value=0.0, max_value=60.0, value=27.9, step=0.1)
amort = st.sidebar.number_input(t("amort", lang), min_value=1, value=12, step=1)

# --- MODELLO DI CALCOLO ---
food = foodcost / 100.0
tax_rate = tax / 100.0
contrib = price * (1 - food)                         # margine di contribuzione per pizza
staff_alloc = staff_cost / staff_ratio               # quota costo personale per distributore
opex = rent + power + conn + maint + staff_alloc      # OPEX mensile per distributore


def net_per_machine(pizzas_day):
    gross = contrib * pizzas_day * 30
    pre_tax = gross - opex
    tax_amt = pre_tax * tax_rate if pre_tax > 0 else 0
    return gross, pre_tax - tax_amt


gross_m, net_m = net_per_machine(ppd)
bep_opex_day = (opex / contrib / 30) if contrib > 0 else 0
bep_full_day = ((opex + capex / amort) / contrib / 30) if contrib > 0 else 0
payback_m = (capex / net_m) if net_m > 0 else None

# --- KPI ---
st.subheader(t("kpi_title", lang))
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric(t("k_gross", lang), fmt(gross_m, lang) + " \u20AC")
c2.metric(t("k_net", lang), fmt(net_m, lang) + " \u20AC")
c3.metric(t("k_bep_opex", lang), fmt(bep_opex_day, lang, 1))
c4.metric(t("k_bep_full", lang), fmt(bep_full_day, lang, 1))
c5.metric(t("k_payback", lang),
          (fmt(payback_m, lang, 1) + " " + t("months", lang)) if payback_m else t("na", lang))

st.divider()

# --- GRAFICI ---
g1, g2 = st.columns(2)

# Utile netto in funzione delle pizze/giorno, con marcatore del pareggio
with g1:
    st.markdown("**" + t("net_title", lang) + "**")
    x_max = max(60, int(ppd * 2))
    xs = list(range(0, x_max + 1))
    ys = [net_per_machine(x)[1] for x in xs]
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name=t("net_line", lang),
                              line=dict(color="#FF7A1A", width=3)))
    fig1.add_hline(y=0, line_dash="dot", line_color="#C9BCA8")
    if bep_opex_day <= x_max:
        fig1.add_vline(x=bep_opex_day, line_dash="dash", line_color="#E0402F")
        fig1.add_trace(go.Scatter(x=[bep_opex_day], y=[0], mode="markers",
                                  name=t("bep_marker", lang),
                                  marker=dict(color="#E0402F", size=11)))
    fig1.update_layout(template="plotly_dark", height=380,
                       margin=dict(l=10, r=10, t=10, b=10),
                       xaxis_title=t("net_x", lang), yaxis_title=t("net_y", lang),
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig1, use_container_width=True)

# Flusso di cassa cumulato di rete con marcatura del mese di rientro
with g2:
    st.markdown("**" + t("cf_title", lang) + "**")
    net_net = net_m * n_machines
    capex_net = capex * n_machines
    horizon = 24
    months_axis = list(range(0, horizon + 1))
    cum = [-capex_net + net_net * mth for mth in months_axis]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=months_axis, y=cum, mode="lines", name=t("cf_line", lang),
                              line=dict(color="#FFC15C", width=3)))
    fig2.add_hline(y=0, line_dash="dot", line_color="#C9BCA8")
    if net_net > 0:
        bep_month = capex_net / net_net
        if bep_month <= horizon:
            fig2.add_vline(x=bep_month, line_dash="dash", line_color="#E0402F")
            fig2.add_trace(go.Scatter(x=[bep_month], y=[0], mode="markers",
                                      name=t("cf_bep", lang),
                                      marker=dict(color="#E0402F", size=11)))
    fig2.update_layout(template="plotly_dark", height=380,
                       margin=dict(l=10, r=10, t=10, b=10),
                       xaxis_title=t("cf_x", lang), yaxis_title=t("cf_y", lang),
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig2, use_container_width=True)

st.caption(t("network_note", lang))
st.divider()

# --- ANALISI PER SCENARI ---
st.subheader(t("scen_title", lang))
scenarios = [
    (t("scen_low", lang), max(1, round(ppd * 0.5))),
    (t("scen_base", lang), ppd),
    (t("scen_high", lang), round(ppd * 1.67)),
]
rows = []
for name, sp in scenarios:
    g, n = net_per_machine(sp)
    rev = price * sp * 30
    pay = (capex / n) if n > 0 else None
    rows.append({
        t("scen_name", lang): name,
        t("scen_ppd", lang): sp,
        t("scen_rev", lang): fmt(rev, lang) + " \u20AC",
        t("scen_net", lang): fmt(n, lang) + " \u20AC",
        t("scen_pay", lang): fmt(pay, lang, 1) if pay else t("na", lang),
    })
st.table(pd.DataFrame(rows))

st.info(t("net_note", lang))
