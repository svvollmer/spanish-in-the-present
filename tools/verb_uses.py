"""How the common verbs are actually used, as short sentences.

A conjugation table tells you how to build `supiéramos`. It does not tell you that `saber` in the
preterite means *found out*, that `quedar` means four unrelated things, or that `buscar` takes no
preposition. Those are what stop you understanding a sentence you have technically parsed, so on
the verb card they go **above** the paradigm.

Only verbs whose use is not obvious from the English gloss are here. `hablar` and `vivir` mean
what they look like and are left alone; `dejar` and `llevar` are not, and are not.

Each entry is a list of (use, spanish, english):
    use      a short label for what the verb is doing, written for a learner
    spanish  a short, everyday sentence. MUST contain a real form of this verb -- build_verbs.py
             checks it against the generated paradigm and fails the build otherwise, so a
             sentence attached to the wrong verb cannot ship.
    english  a natural translation

Deliberately plain vocabulary throughout: the sentence exists to show the verb, not to teach
three new nouns at the same time.
"""

# Forms the paradigm does not contain but the language does. `hay` is corrected to the auxiliary
# `ha` in build_verbs.py because the card shows the auxiliary, so it has to be allowed back here.
EXTRA_FORMS = {"haber": ["hay"]}

USES = {
    "ser": [
        ("who or what something is", "Es ingeniero.", "He's an engineer."),
        ("where someone is from", "Somos de Panamá.", "We're from Panama."),
        ("when an event happens", "La reunión es a las tres.", "The meeting is at three."),
    ],
    "estar": [
        ("where something is", "¿Dónde está el baño?", "Where's the toilet?"),
        ("how someone is right now", "Está cansado.", "He's tired."),
        ("a state that could change", "La tienda está cerrada.", "The shop is closed."),
    ],
    "haber": [
        ("there is / there are — always 'hay', never 'hays'", "Hay dos cuartos.", "There are two rooms."),
        ("the auxiliary for 'have done'", "Ha llamado tres veces.", "He's called three times."),
        ("hay que + infinitive = one has to", "Hay que esperar.", "We'll have to wait."),
    ],
    "tener": [
        ("states English does with 'be'", "Tengo hambre.", "I'm hungry."),
        ("age", "Tengo cuarenta años.", "I'm forty."),
        ("tener que = have to", "Tengo que irme.", "I have to go."),
    ],
    "saber": [
        ("know a fact", "No sé su nombre.", "I don't know his name."),
        ("know how to do something", "¿Sabes nadar?", "Can you swim?"),
        ("in the preterite it means found out", "Lo supe ayer.", "I found out yesterday."),
    ],
    "conocer": [
        ("know a person or place", "No conozco a su hermano.", "I don't know his brother."),
        ("in the preterite it means met", "La conocí en Lima.", "I met her in Lima."),
    ],
    "poder": [
        ("can, be able to", "¿Puedes ayudarme?", "Can you help me?"),
        ("in the preterite it means managed to", "Pude entrar.", "I managed to get in."),
    ],
    "querer": [
        ("want", "Quiero un café.", "I want a coffee."),
        ("negative preterite means refused", "No quiso venir.", "He refused to come."),
    ],
    "quedar": [
        ("arrange to meet", "Quedamos a las ocho.", "We're meeting at eight."),
        ("have left", "Me quedan dos.", "I have two left."),
        ("be situated", "Queda lejos.", "It's a long way away."),
    ],
    "dejar": [
        ("leave something behind", "Dejé el libro en casa.", "I left the book at home."),
        ("let someone do something", "Déjame ver.", "Let me see."),
        ("dejar de = stop doing", "Dejó de fumar.", "He stopped smoking."),
    ],
    "llevar": [
        ("how long you have been somewhere", "Llevo dos años aquí.", "I've been here two years."),
        ("give someone a lift, take something along", "¿Me llevas?", "Can you give me a lift?"),
        ("be wearing", "Lleva una chaqueta azul.", "He's wearing a blue jacket."),
    ],
    "pasar": [
        ("happen", "¿Qué pasó?", "What happened?"),
        ("come in", "Pase, por favor.", "Come in, please."),
        ("go past or drop by", "Pasé por tu casa.", "I went by your place."),
    ],
    "poner": [
        ("put", "Pon la mesa.", "Set the table."),
        ("ponerse = become, suddenly", "Se puso nervioso.", "He got nervous."),
        ("ponerse = put clothes on", "Ponte el abrigo.", "Put your coat on."),
    ],
    "sacar": [
        ("take out", "Saca la basura.", "Take the rubbish out."),
        ("get a mark or a result", "Sacó buenas notas.", "She got good marks."),
    ],
    "tocar": [
        ("play an instrument", "Toca la guitarra.", "He plays the guitar."),
        ("be someone's turn", "Me toca a mí.", "It's my turn."),
    ],
    "hacer": [
        ("weather", "Hace frío.", "It's cold."),
        ("ago", "Hace dos años.", "Two years ago."),
        ("do or make", "¿Qué haces?", "What are you doing?"),
    ],
    "dar": [
        ("da igual = it makes no difference", "Da igual.", "It doesn't matter."),
        ("a window or door facing something", "La ventana da al patio.", "The window faces the yard."),
        ("give you a feeling", "Me dio miedo.", "It scared me."),
    ],
    "ir": [
        ("ir a + infinitive = going to", "Voy a llamarla.", "I'm going to call her."),
        ("how things are going", "¿Cómo te va?", "How's it going?"),
    ],
    "venir": [
        ("come", "Viene de Lima.", "She's coming from Lima."),
        ("venir bien = suit, be handy", "Me viene bien el lunes.", "Monday works for me."),
    ],
    "volver": [
        ("come back", "Vuelvo en cinco minutos.", "I'll be back in five minutes."),
        ("volver a = do something again", "Volvió a llamar.", "He called again."),
    ],
    "seguir": [
        ("still be doing something", "Sigue lloviendo.", "It's still raining."),
        ("keep going, carry straight on", "Siga recto.", "Carry straight on."),
    ],
    "acabar": [
        ("acabar de = have just done", "Acabo de llegar.", "I've just arrived."),
        ("run out", "Se acabó el agua.", "The water ran out."),
    ],
    "parecer": [
        ("seem", "Parece caro.", "It looks expensive."),
        ("what someone thinks of something", "¿Qué te parece?", "What do you think?"),
    ],
    "gustar": [
        ("the thing liked is the subject", "Me gusta el café.", "I like coffee."),
        ("plural thing, plural verb", "Me gustan los dos.", "I like both of them."),
    ],
    "deber": [
        ("ought to, must", "Debo irme.", "I should go."),
        ("deber de = probably", "Debe de estar cansado.", "He must be tired."),
    ],
    "pedir": [
        ("ask for, order", "Pedí un café.", "I ordered a coffee."),
    ],
    "preguntar": [
        ("ask a question — not the same verb as 'ask for'", "Preguntó por ti.", "He asked about you."),
    ],
    "tomar": [
        ("drink, or take in general", "Tomo café por la mañana.", "I drink coffee in the morning."),
        ("catch transport", "Toma el autobús.", "Take the bus."),
    ],
    "mirar": [
        ("look at, on purpose", "Mira esto.", "Look at this."),
    ],
    "ver": [
        ("see", "¿Ves la diferencia?", "Can you see the difference?"),
        ("nos vemos = see you", "Nos vemos el lunes.", "See you Monday."),
    ],
    "salir": [
        ("leave, go out", "Salgo a las seis.", "I leave at six."),
        ("turn out a certain way", "Todo salió bien.", "Everything turned out fine."),
    ],
    "llegar": [
        ("arrive", "Llegó tarde.", "He arrived late."),
        ("llegar a = reach something", "Llegamos a un acuerdo.", "We reached an agreement."),
    ],
    "traer": [
        ("bring, towards the speaker", "¿Me traes agua?", "Could you bring me some water?"),
    ],
    "contar": [
        ("tell", "Cuéntame.", "Tell me about it."),
        ("contar con = count on", "Cuenta conmigo.", "Count on me."),
    ],
    "tratar": [
        ("tratar de = try to", "Trata de dormir.", "Try to sleep."),
        ("se trata de = it's about", "Se trata de dinero.", "It's about money."),
    ],
    "resultar": [
        ("turn out to be", "Resultó más caro.", "It turned out more expensive."),
    ],
    "encontrar": [
        ("find", "No encuentro las llaves.", "I can't find my keys."),
        ("encontrarse = feel, or run into someone", "Me encontré con tu hermana.", "I ran into your sister."),
    ],
    "esperar": [
        ("wait", "Espera un momento.", "Wait a moment."),
        ("hope — the same verb", "Espero que sí.", "I hope so."),
    ],
    "servir": [
        ("be useful, work", "Esto no sirve.", "This is no good."),
        ("servir para = be for", "¿Para qué sirve?", "What's it for?"),
    ],
    "valer": [
        ("be worth, cost", "¿Cuánto vale?", "How much is it?"),
        ("valer la pena = be worth it", "Vale la pena.", "It's worth it."),
    ],
    "caber": [
        ("fit", "No cabe en el coche.", "It doesn't fit in the car."),
    ],
    "decir": [
        ("say, tell", "¿Qué dijiste?", "What did you say?"),
        ("dime = tell me", "Dime la verdad.", "Tell me the truth."),
    ],
    "creer": [
        ("think, believe", "Creo que sí.", "I think so."),
    ],
    "llamar": [
        ("call someone", "Te llamo mañana.", "I'll call you tomorrow."),
        ("llamarse = be called", "Me llamo Ana.", "My name is Ana."),
    ],
    "pensar": [
        ("pensar en = think about", "Pienso en ti.", "I think about you."),
        ("pensar + infinitive = plan to", "Pienso ir el lunes.", "I'm planning to go on Monday."),
    ],
    "sentir": [
        ("lo siento = I'm sorry", "Lo siento mucho.", "I'm very sorry."),
        ("sentirse = feel", "Me siento mal.", "I feel ill."),
    ],
    "empezar": [
        ("empezar a = start doing", "Empezó a llover.", "It started raining."),
    ],
    "buscar": [
        ("look for — no preposition, unlike English", "Busco un hotel.", "I'm looking for a hotel."),
    ],
}
