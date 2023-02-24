# Ce script regroupe les fonctions permettant de calculer les indicateurs en fonction des paramètres donnés

# IMPORTS :


# CONSTANTES :


# FONCTIONS SOLAIRE :

# Structure des paramètres :
# {
#   surface : int   (en km² ?)
# }

def ind_solar(params: dict, perc: float) -> tuple[float] :
    """
    Fonction renvoyant les économies de C02, le ROI et l'investissement
    pour les paramètres donnés, pour le pourcentage de toit couvert donné.
    Le pourcentage `perc` est un flottant compris entre 0 et 1 (inclus).
    """

    CO2 = perc
    ROI = perc
    Inv = perc

    return CO2, ROI, Inv

def solar(params: dict, step=0.01) -> tuple[list[float]] :
    """
    Fonction renvoyant 3 listes d'indicateurs (CO2, ROI, Inv) en fonction du % de toit couvert.
    """

    CO2, ROI, INV = [], [], []

    for p in range(0, 1, step) :
        co2, roi, inv = ind_solar(params, p)
        CO2.append(co2)
        ROI.append(roi)
        INV.append(inv)
    
    return CO2, ROI, INV


# FONCTIONS LEDS

# Structure des paramètres :
# {
#   perc_var : float (%)
#   perc_det : float (%)
# }

def ind_leds(params: dict, perc: float) -> tuple[float] :
    """
    Fonction renvoyant les économies de C02, le ROI et l'investissement
    pour les paramètres donnés, et du pourcentage d'éclairage LED.
    Le pourcentage `perc` est un flottant compris entre 0 et 1 (inclus).
    """

    # Partie à modifier pour le calcul :
    CO2 = perc
    ROI = perc
    Inv = perc
    # Fin de la partie à modifier

    return CO2, ROI, Inv

def leds(params: dict, step=0.01) -> tuple[list[float]] :
    """
    Fonction renvoyant 3 listes d'indicateurs (CO2, ROI, Inv) en fonction du % de toit couvert.
    """

    CO2, ROI, INV = [], [], []

    for p in range(0, 1, step) :
        co2, roi, inv = ind_leds(params, p)
        CO2.append(co2)
        ROI.append(roi)
        INV.append(inv)
    
    return CO2, ROI, INV