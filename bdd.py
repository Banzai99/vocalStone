from decimal import Decimal
from peewee import *
from peewee import RawQuery

bdd = MySQLDatabase('G223_B_BD2', user='G223_B', password='G223_B',host='pc-tp-mysql.insa-lyon.fr', port=3306)
#bdd = PostgresqlDatabase('p2i', user='p2i', password='wheatstone', host='vps.ribes.ovh', port=5432)
bdd.connect()

class Personne(Model):
    class Meta:
        database = bdd
    nom = CharField(max_length=255, unique=True)

class Echantillon(Model):
    """
    Cette classe contient la liste des coefficients de fourier dans une chaîne de caractère et avec des foerign keys
    utiliser ``_liste_coefs`` pour faire les requêtes et ``liste_coefs``pour les opéeations Python
    """
    class Meta:
        database = bdd
    personne = ForeignKeyField(Personne, backref='echantillons')
    _liste_coefs = CharField(max_length=4095,column_name='liste_coefs') #liste des coefficients de fourier séparés par des virgules

    @property
    def liste_coefs(self):
        return self._liste_coefs #c'est comme ça qu'on fait les getters en python

    @liste_coefs.setter
    def liste_coefs(self, liste_coefs):
        self._liste_coefs = liste_coefs
        self.save()
        i=1
        Coef.delete().where(Coef.echantillon == self).execute()
        for x in liste_coefs.split(','):
            Coef.create(echantillon=self, coef_id=i, valeur=x)
            i+=1

class Coef(Model):
    class Meta:
        database = bdd
    echantillon = ForeignKeyField(Echantillon, backref='coefs')
    valeur = DecimalField()
    coef_id = IntegerField()


#bdd.create_tables([Personne, Echantillon, Coef])
jean = Personne.select().where(Personne.nom == "Jean").get() #jean = Personne.create(nom="Jean")
#jean_ech1 = Echantillon.create(
#    personne=jean,
#    liste_coefs="35712.0, 4041.823759526427, 1810.3397560507735, 726.233028946459, 480.676137555932, 548.881695829304, 599.875476252882, 125.52710062001802, 159.33541845923656, 118.48399994986221, 229.38243601730713, 254.28742980414154, 280.09852873821626, 14.540801756079144, 136.71934082807434, 218.91438714438135, 153.3907925161573, 85.008944542027, 109.85958852814588, 139.69963528948495, 93.12192424052698, 147.90802593303945, 100.04355012744868, 46.89957223359737, 122.30897943339971, 77.95036706450564, 107.2412474002416, 103.7922163828542, 46.52520797326243, 92.58831922129706, 2.9399427693122506, 22.618714993487945, 51.36558622539378, 51.034157042539384, 53.12749367262431, 63.102596817676115, 89.0280455830212, 54.605739960575185, 102.55251800153789, 64.82746757634386, 47.65659535403987, 35.55984448369428, 36.69744244101786, 58.76595228733454, 22.24884031325586, 17.48422253672434, 60.600656374381174, 69.03418221189571, 70.5275227789426, 14.678223847353093, 37.3253316182498, 51.99785832114796, 41.79977334502167, 32.214038379252855, 23.14064339797962, 55.354475559192124, 66.74189638293699, 66.61956013948179, 57.26836540651857, 46.6616933118907, 70.27406858009756, 47.47124034240958, 44.61726813190782, 38.806674818265, 118.6001686339442, 27.535353651334308, 61.86915175781595, 35.66372829849509, 47.356011930739285, 59.86800737059462, 76.4200539615342, 67.30354797613666, 53.79985880161167, 12.354551132452825, 66.28215398677594, 43.01165609345055, 52.27757850447904, 76.43107172481928, 78.07059610151805, 55.34173084304209, 55.23503112963858, 141.12902168417392, 44.853136730210736, 88.10997795588129, 2.0893406572278703, 67.0808329699994, 29.736147105960164, 35.43473886262422, 41.677115532629315, 59.18361157580167, 91.41612113333782, 112.42786880475687, 42.066099216650485, 97.89669352837367, 20.708657325097604, 52.87466787616364, 43.33101143201757, 75.40138655252802, 31.29594938130617, 75.46334949309431, 62.45463216312818, 93.92772410843656, 61.79523226564402, 127.37631712941281, 72.75825377044681, 84.22958265154969, 27.43449690905421, 96.46637510185339, 50.69518000847108, 32.83241480741757, 161.30185076108367, 62.57408043915021, 108.76683611303024, 91.67323112782532, 58.860110829846704, 82.84436869475937, 59.637550970621795, 43.47991772328409, 17.64319455446452, 24.019000501010584, 73.60662947678398, 43.851687082985585, 10.890438781278775, 60.23138008701861, 47.66160615433755, 16.179062315399914, 106.77370752862882, 87.22658260478322"
#)
jean_ech1 = Echantillon.get(Echantillon.personne == jean)
i=1

#for c in jean_ech1.liste_coefs.split(','): #on itère les valeurs de la liste des coefficients de l'Échantillon
#    Coef.create(echantillon=jean_ech1, valeur=Decimal(c), coef_id=i)
#    i+=1 #pour avoir une numérotation du coefficient dans l'échantillon

for row in RawQuery(sql="SELECT * FROM personne").bind(bdd).execute():
    personne = Personne(**row) #on transforme {'id':1, 'nom':'bastian'} en Personne(id=1, nom="bastian"), ça s'applelle l'unpacking
    print(personne.nom)