import pymongo

def db(name='Users', collection='data'):
  cluster = pymongo.MongoClient('YOUR_MONGODB_URI')
  
  db = cluster.get_database(name)
  
  udata = db.get_collection(collection)
  return udata

udb = db()

def readSet(uid, val, default=0, db=udb):
    # Fazer a consulta no MongoDB usando o uid como filtro (sem projeção)
    document = db.find_one({"uid": uid})

    # Verificar se o campo aninhado existe no documento
    nested_value = document
    nested_fields = val.split('.')
    for field in nested_fields:
        if isinstance(nested_value, dict) and field in nested_value:
            nested_value = nested_value[field]
        else:
            # Caso o campo aninhado não exista, insere o campo com o valor padrão no banco de dados
            nested_value = default
            break
    else:
        # Caso todos os campos aninhados existam, retornamos o valor encontrado
        return nested_value

    # Caso o documento não seja encontrado ou o campo aninhado não exista, insere o campo com o valor padrão no banco de dados
    db.update_one({"uid": uid}, {"$set": {val: default}}, upsert=True)
    return default

