from kafka import KafkaProducer

host = "localhost:9094"
producer = KafkaProducer(bootstrap_servers=host)
for article_id in ["nphys177", "nphys151", "nphys152", "nphys153", "nphys154", "nphys155", "nphys156"]:
    print("sending..", article_id)
    producer.send("article", str.encode(article_id))
producer.flush()