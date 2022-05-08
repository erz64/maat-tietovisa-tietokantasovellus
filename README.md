# Maantieto Visa

## Sovelluksen tarkoitus

- Sovellus on netissä toimiva maantieto visailupeli, jossa on muutamia tietovisoja, joissa kaikissa pitää arvata kyseinen maa esimerkiksi maan pääkaupungin kuvasta tai maan kansallisruoasta
Sovelluksen ominaisuudet:
- Sovellusta voi testata [herokussa](https://maat-tietovisa.herokuapp.com/)
- Sovelluksessa kolme eri tietovisaa
- Tietovisassa sivulla näytetään kysymys, kuva, ja top 3 parhaat tulokset, ja käyttäjän pitää arvata näiden perusteella kyseinen maa
- Tietovisan kysymykset tulevat satunnaisesti ja sama kysymys ei voi tulla kahta kertaa samassa visassa
- Visassa on kymmenen kysymystä, ja näihin vastattua hän saa tietää tuloksensa, ja jos hänen tuloksensa on parempi kuin hänen viimeinen tuloksensa ja se yltää kol,em parhaimman joukkoon, hän pääsee highscores listalle, joka näytetään visojen yhteydessä
- Käyttäjä voi luoda etusivulla käyttäjän itselleen ja kirjautua sisään
- Questions ja images tietokantoihin voidaan lisätä kysymys ja kuva [täältä](https://maat-tietovisa.herokuapp.com/form), vain käyttäjät joilla on admin role voivat päästä tälle sivulle. Uusia admin käyttäjiä ei voida tehdä ilman ylläpitäjää. Jos haluaa kuitenkin testata järkevän kuvan ja kysymyksen lisäystä visoihin yksi admin käyttäjistä on: Käyttäjänimi: erz, salasana: tietokanta-sovellus
- Käyttäjä voi arvioida visan yhdestä viiteen tähteä visan lopussa, nämä arviot näytetään etusivulla visan linkin yhteydessä