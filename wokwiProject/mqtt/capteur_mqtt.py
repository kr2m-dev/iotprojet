import paho.mqtt.client as mqtt
import time, random, math, json, ssl

# ============================================
# CONFIGURATION HIVEMQ
# ============================================
BROKER   = "74e9d04cfff84051b0ee439bf05bf6ca.s1.eu.hivemq.cloud"
PORT     = 8883
USERNAME = "iot_eau"
PASSWORD = "Passer@1234"
INTERVAL = 5

# ============================================
# Simulation capteurs (même logique que HTTP)
# ============================================
def simuler_ph(t):
    return round(7.2 + math.sin(t * 0.3) * 0.4 + random.uniform(-0.05, 0.05), 2)

def simuler_turbidite(t):
    return round(max(0, 1.5 + math.sin(t * 0.2) * 1.0 + random.uniform(-0.1, 0.1)), 2)

def simuler_temperature(t):
    return round(26.0 + math.sin(t * 0.1) * 2.0 + random.uniform(-0.2, 0.2), 2)

# ============================================
# Callbacks MQTT
# ============================================
def on_connect(client, userdata, flags, rc):
    codes = {
        0: "Connecté avec succès",
        1: "Mauvaise version protocole",
        2: "Identifiant refusé",
        3: "Serveur indisponible",
        4: "Mauvais username/password",
        5: "Non autorisé"
    }
    print(f"[MQTT] {codes.get(rc, f'Code inconnu: {rc}')}")

def on_publish(client, userdata, mid):
    print(f"       Message #{mid} confirmé par le broker")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"[MQTT] Déconnexion inattendue (code {rc}), reconnexion...")

# ============================================
# Connexion au broker
# ============================================
client = mqtt.Client(client_id="capteur_forage1", protocol=mqtt.MQTTv311)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.on_connect    = on_connect
client.on_publish    = on_publish
client.on_disconnect = on_disconnect

print("=" * 55)
print("  Simulateur capteur eau — MQTT vers HiveMQ Cloud")
print(f"  Broker : {BROKER}:{PORT}")
print(f"  Topics : eau/forage1/ph | turbidite | temperature")
print("=" * 55)

client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

time.sleep(2)  # laisser la connexion s'établir

# ============================================
# Boucle principale
# ============================================
t = 0
cycle = 0

print("Appuie sur Ctrl+C pour arrêter\n")

try:
    while True:
        t += 1
        cycle += 1

        ph          = simuler_ph(t)
        turbidite   = simuler_turbidite(t)
        temperature = simuler_temperature(t)

        # Vérification alertes
        alertes = []
        if ph < 6.5 or ph > 8.5:
            alertes.append(f"pH hors norme ({ph})")
        if turbidite > 4:
            alertes.append(f"Turbidité élevée ({turbidite} NTU)")
        if temperature > 30:
            alertes.append(f"Température élevée ({temperature}°C)")

        # Publication sur chaque topic séparé
        client.publish(f"eau/forage1/ph",          str(ph),          qos=1)
        client.publish(f"eau/forage1/turbidite",   str(turbidite),   qos=1)
        client.publish(f"eau/forage1/temperature", str(temperature), qos=1)

        # Publication JSON groupé (pour Node-RED)
        payload_json = json.dumps({
            "point_id":    "forage1",
            "ph":          ph,
            "turbidite":   turbidite,
            "temperature": temperature,
            "alerte":      1 if alertes else 0
        })
        client.publish("eau/forage1/data", payload_json, qos=1)

        statut = f"⚠  ALERTE : {', '.join(alertes)}" if alertes else "✓  Normal"
        print(f"[Cycle {cycle:03d}] pH={ph}  Turb={turbidite}  Temp={temperature}°C  {statut}")

        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\nArrêt du simulateur.")
    client.loop_stop()
    client.disconnect()