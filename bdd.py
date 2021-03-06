from datetime import datetime
from io import BytesIO

import numpy
from peewee import *
from peewee import RawQuery

maBDD = MySQLDatabase('G223_B_BD2', user='G223_B', password='G223_B', host='pc-tp-mysql.insa-lyon.fr', port=3306)
# maBDD = PostgresqlDatabase('p2i', user='p2i', password='wheatstone', host='vps.ribes.ovh', port=5432)
try:
    maBDD.connect()
except OperationalError:
    print("Base de donnée non disponible !")


# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

class Personne(Model):
    class Meta:
        database = maBDD

    nom = CharField(max_length=255, unique=True)
    autorisee = BooleanField(column_name='autorise', default=False)


class Echantillon(Model):
    """
    Cette classe contient la liste des coefficients de fourier dans une chaîne de caractère et avec des foerign keys
    utiliser ``_liste_coefs`` pour faire les requêtes et ``liste_coefs``pour les opéeations Python
    """

    class Meta:
        database = maBDD

    personne = ForeignKeyField(Personne, backref='echantillons')
    nom_echantillon = CharField(max_length=255)

    @property
    def matrice(self) -> numpy.array:
        morceaux = []
        for morceau in self.morceaux:
            morceaux.append(morceau.coefs)
        return numpy.array(morceaux)


class Morceau(Model):
    class Meta:
        database = maBDD

    # def __init__(self, echantiloon, _coefs, **kwargs):
    # def __init__(self, **kwargs):
    #    self.coefs = kwargs.get('coefs', None)
    #    super().__init__(**kwargs)
    echantillon = ForeignKeyField(Echantillon, backref='morceaux')
    _coefs = BlobField()

    @property
    def coefs(self):
        return numpy.load(BytesIO(self._coefs))

    @coefs.setter
    def coefs(self, coefs: numpy.array):
        with BytesIO() as b:
            numpy.save(b, coefs)
            self._coefs = b.getvalue()


class Entree(Model):
    class Meta:
        database = maBDD

    personne = ForeignKeyField(Personne, backref='historique')
    horodatage = DateTimeField(default=datetime.now)  # pas besoin de le remplir du coup
    pourcentage_confiance = IntegerField()  # entre 0 et 100


# maBDD.create_tables([Personne, Echantillon, Morceau])
# jean = Personne.select().where(Personne.nom == "Jean").get() #jean = Personne.create(nom="Jean")
# jean_ech1 = Echantillon.create(
#    personne=jean,
#    liste_coefs="35712.0, 4041.823759526427, 1810.3397560507735, 726.233028946459, 480.676137555932, 548.881695829304, 599.875476252882, 125.52710062001802, 159.33541845923656, 118.48399994986221, 229.38243601730713, 254.28742980414154, 280.09852873821626, 14.540801756079144, 136.71934082807434, 218.91438714438135, 153.3907925161573, 85.008944542027, 109.85958852814588, 139.69963528948495, 93.12192424052698, 147.90802593303945, 100.04355012744868, 46.89957223359737, 122.30897943339971, 77.95036706450564, 107.2412474002416, 103.7922163828542, 46.52520797326243, 92.58831922129706, 2.9399427693122506, 22.618714993487945, 51.36558622539378, 51.034157042539384, 53.12749367262431, 63.102596817676115, 89.0280455830212, 54.605739960575185, 102.55251800153789, 64.82746757634386, 47.65659535403987, 35.55984448369428, 36.69744244101786, 58.76595228733454, 22.24884031325586, 17.48422253672434, 60.600656374381174, 69.03418221189571, 70.5275227789426, 14.678223847353093, 37.3253316182498, 51.99785832114796, 41.79977334502167, 32.214038379252855, 23.14064339797962, 55.354475559192124, 66.74189638293699, 66.61956013948179, 57.26836540651857, 46.6616933118907, 70.27406858009756, 47.47124034240958, 44.61726813190782, 38.806674818265, 118.6001686339442, 27.535353651334308, 61.86915175781595, 35.66372829849509, 47.356011930739285, 59.86800737059462, 76.4200539615342, 67.30354797613666, 53.79985880161167, 12.354551132452825, 66.28215398677594, 43.01165609345055, 52.27757850447904, 76.43107172481928, 78.07059610151805, 55.34173084304209, 55.23503112963858, 141.12902168417392, 44.853136730210736, 88.10997795588129, 2.0893406572278703, 67.0808329699994, 29.736147105960164, 35.43473886262422, 41.677115532629315, 59.18361157580167, 91.41612113333782, 112.42786880475687, 42.066099216650485, 97.89669352837367, 20.708657325097604, 52.87466787616364, 43.33101143201757, 75.40138655252802, 31.29594938130617, 75.46334949309431, 62.45463216312818, 93.92772410843656, 61.79523226564402, 127.37631712941281, 72.75825377044681, 84.22958265154969, 27.43449690905421, 96.46637510185339, 50.69518000847108, 32.83241480741757, 161.30185076108367, 62.57408043915021, 108.76683611303024, 91.67323112782532, 58.860110829846704, 82.84436869475937, 59.637550970621795, 43.47991772328409, 17.64319455446452, 24.019000501010584, 73.60662947678398, 43.851687082985585, 10.890438781278775, 60.23138008701861, 47.66160615433755, 16.179062315399914, 106.77370752862882, 87.22658260478322"
# )
# jean_ech1 = Echantillon.get(Echantillon.personne == jean)

# i=1
# for c in jean_ech1.liste_coefs.split(','): #on itère les valeurs de la liste des coefficients de l'Échantillon
#    Coef.create(echantillon=jean_ech1, valeur=Decimal(c), coef_id=i)
#    i+=1 #pour avoir une numérotation du coefficient dans l'échantillon

# for row in RawQuery(sql="SELECT * FROM personne").bind(bdd).execute():
#    personne = Personne(**row) #on transforme {'id':1, 'nom':'bastian'} en Personne(id=1, nom="bastian"), ça s'applelle l'unpacking
#    print(personne.nom)

# requete pour voir les enregistrements
# select p.nom, e.nom_echantillon, count(m.id) from personne as p, echantillon as e, morceau as m where m.echantillon_id = e.id and e.personne_id = p.id group by m.echantillon_id;

# select p.nom, count(e.id) from personne as p, echantillon as e where e.personne_id = p.id group by p.id;

def enregistrer_entree_historique(classe_pred: str, probas: dict, autorise: bool):
    pers = Personne.get(Personne.nom == classe_pred)
    if autorise:
        Entree.create(personne=pers, pourcentage_confiance=probas[classe_pred])
    return classe_pred, probas, autorise


def historique_entrees_par_jour():# -> List[Dict[int, date, int]]:
    donnees = RawQuery(
        sql="SELECT COUNT(e.id) as n_entrees, DATE(e.horodatage) as jour, min(e.pourcentage_confiance) as conf_min, AVG(e.pourcentage_confiance) as conf_avg from entree as e group by date(e.horodatage);"
    ).bind(maBDD).execute()
    a = list(donnees)
    #print(a)
    return a

def historique_jour_et_nom_rollup():
    rows = RawQuery(
        sql="SELECT date(e.horodatage) as jour, p.nom as nom, count(e.id) as n_entrees, min(e.pourcentage_confiance) as conf_min, AVG(e.pourcentage_confiance) as conf_avg from entree as e, personne as p where p.id=e.personne_id group by date(e.horodatage), p.nom with rollup;"
    ).bind(maBDD).execute()
    return rows