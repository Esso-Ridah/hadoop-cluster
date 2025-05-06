#!/usr/bin/env python3
import json
import os
from airflow import settings
from airflow.models import Connection
from sqlalchemy.orm import Session

def import_connections():
    # 1) Charge le JSON depuis AIRFLOW_HOME/config/connections.json
    config_dir = os.getenv('AIRFLOW_HOME', '/opt/airflow') + '/config'
    path = os.path.join(config_dir, 'connections.json')
    if not os.path.isfile(path):
        print(f"⚠️  Fichier non trouvé : {path}")
        return

    with open(path) as f:
        data = json.load(f)

    # 2) Détermine si c'est une liste ou un dict
    if isinstance(data, dict):
        connections = list(data.values())
    elif isinstance(data, list):
        connections = data
    else:
        raise ValueError("Le fichier connections.json doit être un list ou un dict racine")

    # 3) Ouvre la session
    session: Session = settings.Session()
    for conn in connections:
        cid = conn.get('conn_id')
        if not cid:
            continue
        existing = session.query(Connection).filter_by(conn_id=cid).first()
        if existing:
            print(f"🔄 Update {cid}")
            for attr in ('conn_type','host','login','password','schema','port'):
                if conn.get(attr) is not None:
                    setattr(existing, attr, conn[attr])
            if conn.get('extra') is not None:
                existing.set_extra(conn['extra'])
        else:
            print(f"➕ Create {cid}")
            new = Connection(
                conn_id=cid,
                conn_type=conn.get('conn_type'),
                host=conn.get('host'),
                login=conn.get('login'),
                password=conn.get('password'),
                schema=conn.get('schema'),
                port=conn.get('port'),
            )
            if conn.get('extra'):
                new.set_extra(conn['extra'])
            session.add(new)
    session.commit()
    session.close()
    print("✅ Import terminé")

if __name__ == "__main__":
    import_connections() 