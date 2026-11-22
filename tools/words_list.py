"""The common-word list: the words that actually block comprehension, with their uses.

Hand-authored, not imported. Two reasons:

1. A raw frequency list is the wrong list. At 30-50% listening comprehension the words that
   defeat you are not content nouns -- those are often cognates or guessable from context. They
   are the glue: the one-syllable function words, the discourse markers, and the handful of
   workhorses (`ya`, `lo`, `se`, `que`, `como`) where one short word does four unrelated jobs.
   Frequency rank alone puts `casa` and `ya` near each other; only one of them is hard.

2. Provenance. Most published frequency lists and every dictionary gloss carry licences that do
   not suit a product (see `verbs.json`'s GPL problem in the README). Everything here is written
   for this book, so it is owned outright -- and tuning the examples to the conversations these
   learners actually have is better teaching anyway.

Each entry:
    w       headword, or a multi-word expression
    pos     part of speech, for filtering
    grp     which group it is browsed under
    tier    1 = you will hear this constantly and must not hesitate
            2 = common, and worth owning once tier 1 is automatic
    senses  the uses. ORDER MATTERS: most frequent sense first.
            g   the gloss for this use
            ex  a Spanish example. MUST contain the headword -- the cloze drill is generated
                by blanking it, and build_words.py refuses to emit an example that does not.
            en  a natural English translation of ex
            blank  optional. The exact surface form to blank, when the example inflects the
                headword (`medio` -> `Media hectárea`). Real examples inflect; distorting a
                natural sentence to match the dictionary form would be the wrong fix, and
                guessing the inflection in code risks blanking the wrong token.
    note    optional; what a learner gets wrong, or where Latin America differs

Examples lean on the conversations these learners are actually having -- land, prices,
paperwork -- because a sentence you might really hear is remembered and a textbook one is not.
"""

WORDS = [
    # ---------------------------------------------------------------- one word, many jobs
    dict(w="que", pos="conj / pron", grp="One word, many jobs", tier=1,
         senses=[
             dict(g="that (gluing two clauses together)",
                  ex="Dice que viene mañana.", en="He says he's coming tomorrow."),
             dict(g="that / which / who (relative)",
                  ex="El lote que vimos ayer.", en="The lot we saw yesterday."),
             dict(g="than (in comparisons)",
                  ex="Es más caro que el otro.", en="It's more expensive than the other one."),
         ],
         note="`qué` with an accent is the question word. Unstressed `que` is the workhorse that "
              "glues clauses together, and in fast speech it is barely pronounced at all."),

    dict(w="lo", pos="pron / art", grp="One word, many jobs", tier=1,
         senses=[
             dict(g="it (neuter object)", ex="No lo sé.", en="I don't know."),
             dict(g="the ... part (lo + adjective makes an abstract noun)",
                  ex="Lo difícil es el precio.", en="The hard part is the price."),
             dict(g="what (lo que)", ex="No entendí lo que dijo.",
                  en="I didn't understand what he said."),
         ],
         note="`lo` is never 'the' in front of a masculine noun -- that is `el`. With an "
              "adjective it means 'the ... thing', which has no tidy English equivalent."),

    dict(w="ya", pos="adv", grp="One word, many jobs", tier=1,
         senses=[
             dict(g="already", ex="Ya firmamos el contrato.", en="We already signed the contract."),
             dict(g="now, right away", ex="Ya voy.", en="I'm on my way."),
             dict(g="no longer (with a negative)", ex="Ya no vive aquí.",
                  en="He doesn't live here any more."),
         ],
         note="Mostly carried by tone. With `no` it always means 'not any more' -- `ya no` is "
              "worth hearing as a single word."),

    dict(w="se", pos="pron", grp="One word, many jobs", tier=1,
         senses=[
             dict(g="impersonal / passive: one does, it is done",
                  ex="Se vende lote.", en="Lot for sale."),
             dict(g="it happened to me (no one is blamed)",
                  ex="Se me olvidó el recibo.", en="I forgot the receipt."),
             dict(g="reflexive, or a change of state",
                  ex="Se puso nervioso.", en="He got nervous."),
             dict(g="stands in for le / les before lo / la",
                  ex="Se lo di al dueño.", en="I gave it to the owner."),
         ],
         note="Four unrelated jobs, one syllable. Chapter 10 has the full picture."),

    dict(w="como", pos="conj / prep", grp="One word, many jobs", tier=1,
         senses=[
             dict(g="like, as", ex="Es como el otro terreno.", en="It's like the other plot."),
             dict(g="about, roughly (before a number)",
                  ex="Como veinte metros.", en="About twenty metres."),
             dict(g="since, because (starting a sentence)",
                  ex="Como no llegó, nos fuimos.", en="Since he didn't turn up, we left."),
         ],
         note="`cómo` with an accent asks 'how'. Unstressed `como` means 'like' or 'roughly'."),

    dict(w="mismo", pos="adj / adv", grp="One word, many jobs", tier=1,
         senses=[
             dict(g="same", ex="Es el mismo terreno.", en="It's the same plot."),
             dict(g="-self (emphasis)", ex="Yo mismo lo vi.", en="I saw it myself."),
             dict(g="right (intensifying a time or place)",
                  ex="Ahora mismo.", en="Right now."),
         ]),

    dict(w="nada", pos="pron", grp="One word, many jobs", tier=1,
         senses=[
             dict(g="nothing", ex="No hay nada escrito.", en="There's nothing in writing."),
             dict(g="not at all (para nada)", ex="No me gusta para nada.",
                  en="I don't like it at all."),
         ]),

    dict(w="algo", pos="pron / adv", grp="One word, many jobs", tier=1,
         senses=[
             dict(g="something", ex="Falta algo en el expediente.",
                  en="Something's missing from the file."),
             dict(g="somewhat, a bit", ex="Está algo caro.", en="It's a bit expensive."),
         ]),

    dict(w="tan", pos="adv", grp="One word, many jobs", tier=1,
         senses=[
             dict(g="so, that (before an adjective or adverb)",
                  ex="No es tan caro.", en="It isn't that expensive."),
         ],
         note="`tan` goes before adjectives and adverbs; `tanto` goes with verbs and nouns."),

    dict(w="tanto", pos="adv / det", grp="One word, many jobs", tier=1,
         senses=[
             dict(g="so much, that much", ex="No cuesta tanto.", en="It doesn't cost that much."),
             dict(g="so many (tantos + noun)", ex="No hay tantos compradores.",
                  en="There aren't that many buyers.", blank="tantos"),
         ]),

    # ---------------------------------------------------------------- por and para
    dict(w="por", pos="prep", grp="por and para", tier=1,
         senses=[
             dict(g="because of, for the sake of (a cause)",
                  ex="Lo compré por el terreno.", en="I bought it for the land."),
             dict(g="through, around (vague place)",
                  ex="Pasamos por el centro.", en="We went through the centre."),
             dict(g="per", ex="Dos veces por semana.", en="Twice a week."),
             dict(g="by (who did it)", ex="Firmado por el dueño.", en="Signed by the owner."),
         ]),

    dict(w="para", pos="prep", grp="por and para", tier=1,
         senses=[
             dict(g="for (a recipient or purpose)", ex="Es para ti.", en="It's for you."),
             dict(g="by (a deadline)", ex="Para el lunes.", en="By Monday."),
             dict(g="in order to (before an infinitive)",
                  ex="Para firmar necesito el título.", en="To sign, I need the title."),
         ],
         note="Rule of thumb that survives most cases: `por` looks backwards at a cause, "
              "`para` looks forwards at a goal."),

    # ---------------------------------------------------------------- connectors and glue
    dict(w="aunque", pos="conj", grp="Connectors and glue", tier=1,
         senses=[
             dict(g="although (conceding a fact)", ex="Aunque es caro, me interesa.",
                  en="Although it's expensive, I'm interested."),
             dict(g="even if (with the subjunctive, a hypothetical)",
                  ex="Aunque sea caro, lo quiero.", en="Even if it's expensive, I want it."),
         ],
         note="The verb mood is the whole difference: indicative concedes something true, "
              "subjunctive supposes something that may not be."),

    dict(w="sino", pos="conj", grp="Connectors and glue", tier=1,
         senses=[
             dict(g="but rather (correcting, after a negative)",
                  ex="No es el precio, sino los gastos.",
                  en="It isn't the price, it's the fees."),
         ],
         note="Only after a negative, and it replaces rather than adds. `pero` adds a "
              "qualification; `sino` corrects the thing just denied."),

    dict(w="mientras", pos="conj", grp="Connectors and glue", tier=1,
         senses=[
             dict(g="while", ex="Mientras firmamos, ella esperó afuera.",
                  en="While we signed, she waited outside."),
             dict(g="as long as (with the subjunctive)",
                  ex="Mientras no firmes, no hay trato.",
                  en="As long as you don't sign, there's no deal."),
         ]),

    dict(w="según", pos="prep / conj", grp="Connectors and glue", tier=1,
         senses=[
             dict(g="according to", ex="Según el plano, son mil metros.",
                  en="According to the plan, it's a thousand metres."),
             dict(g="depending on", ex="Según cómo quede, decidimos.",
                  en="Depending on how it turns out, we'll decide."),
         ]),

    dict(w="apenas", pos="adv / conj", grp="Connectors and glue", tier=2,
         senses=[
             dict(g="barely, hardly", ex="Apenas lo conozco.", en="I barely know him."),
             dict(g="as soon as", ex="Apenas llegue, te llamo.",
                  en="As soon as he arrives, I'll call you."),
         ]),

    dict(w="en cuanto", pos="conj", grp="Connectors and glue", tier=2,
         senses=[
             dict(g="as soon as", ex="En cuanto firme, te aviso.",
                  en="As soon as I sign, I'll let you know."),
         ]),

    dict(w="ni", pos="conj", grp="Connectors and glue", tier=1,
         senses=[
             dict(g="not even", ex="Ni lo vi.", en="I didn't even see it."),
             dict(g="neither ... nor", ex="Ni el precio ni los linderos están claros.",
                  en="Neither the price nor the boundaries are clear."),
         ]),

    dict(w="tampoco", pos="adv", grp="Connectors and glue", tier=1,
         senses=[
             dict(g="neither, not either", ex="Yo tampoco lo sabía.",
                  en="I didn't know either."),
         ]),

    dict(w="además", pos="adv", grp="Connectors and glue", tier=1,
         senses=[
             dict(g="besides, what's more", ex="Además, falta el recibo.",
                  en="Besides, the receipt is missing."),
         ]),

    dict(w="encima", pos="adv", grp="Connectors and glue", tier=2,
         senses=[
             dict(g="on top (of)", ex="Está encima de la mesa.", en="It's on top of the table."),
             dict(g="on top of that (piling on a complaint)",
                  ex="Y encima me cobró la notaría.",
                  en="And on top of that he charged me the notary fee."),
         ]),

    dict(w="por eso", pos="conn", grp="Connectors and glue", tier=1,
         senses=[
             dict(g="that's why", ex="Por eso quiero verlo primero.",
                  en="That's why I want to see it first."),
         ]),

    dict(w="ya que", pos="conj", grp="Connectors and glue", tier=2,
         senses=[
             dict(g="since, given that", ex="Ya que estamos aquí, veamos el lindero.",
                  en="Since we're here, let's look at the boundary."),
         ]),

    dict(w="de todas formas", pos="conn", grp="Connectors and glue", tier=2,
         senses=[
             dict(g="anyway, either way", ex="De todas formas hay que firmar.",
                  en="Either way, we have to sign."),
         ]),

    # ---------------------------------------------------------------- amounts and which ones
    dict(w="cada", pos="det", grp="Amounts and which ones", tier=1,
         senses=[
             dict(g="each, every", ex="Cada lote tiene su escritura.",
                  en="Each lot has its own deed."),
         ]),

    dict(w="cualquier", pos="det", grp="Amounts and which ones", tier=2,
         senses=[
             dict(g="any (at all)", ex="Cualquier día de esta semana.",
                  en="Any day this week."),
         ],
         note="`cualquier` goes before a noun; `cualquiera` stands on its own."),

    dict(w="algún", pos="det", grp="Amounts and which ones", tier=1,
         senses=[
             dict(g="some, any", ex="¿Hay algún problema con el título?",
                  en="Is there any problem with the title?"),
         ]),

    dict(w="ningún", pos="det", grp="Amounts and which ones", tier=1,
         senses=[
             dict(g="no, not any", ex="No hay ningún problema.", en="There's no problem."),
         ],
         note="Spanish doubles the negative and both halves are compulsory: `no` on the verb "
              "and `ningún` on the noun. Dropping the `no` sounds wrong, not emphatic."),

    dict(w="otro", pos="det", grp="Amounts and which ones", tier=1,
         senses=[
             dict(g="another, other", ex="Vimos otro lote más barato.",
                  en="We saw another, cheaper lot."),
         ],
         note="Never `un otro`. 'Another' is just `otro`."),

    dict(w="propio", pos="adj", grp="Amounts and which ones", tier=2,
         senses=[
             dict(g="own", ex="Tiene su propio pozo.", en="It has its own well."),
             dict(g="himself, herself (before the noun)",
                  ex="Me lo dijo el propio dueño.", en="The owner himself told me."),
         ]),

    dict(w="demás", pos="det / pron", grp="Amounts and which ones", tier=2,
         senses=[
             dict(g="the rest, the others", ex="Los demás documentos llegan mañana.",
                  en="The rest of the documents arrive tomorrow."),
         ]),

    dict(w="varios", pos="det", grp="Amounts and which ones", tier=2,
         senses=[
             dict(g="several", ex="Hay varios compradores interesados.",
                  en="There are several interested buyers."),
         ]),

    dict(w="bastante", pos="adv / det", grp="Amounts and which ones", tier=1,
         senses=[
             dict(g="quite, fairly", ex="Está bastante lejos del pueblo.",
                  en="It's quite far from the town."),
             dict(g="enough, plenty of", ex="Hay bastante agua.", en="There's plenty of water."),
         ]),

    dict(w="demasiado", pos="adv / det", grp="Amounts and which ones", tier=1,
         senses=[
             dict(g="too, too much", ex="Es demasiado caro para mí.",
                  en="It's too expensive for me."),
         ]),

    dict(w="medio", pos="adj / adv", grp="Amounts and which ones", tier=2,
         senses=[
             dict(g="half", ex="Media hectárea.", en="Half a hectare.", blank="Media"),
             dict(g="kind of, a bit (before an adjective)",
                  ex="El camino está medio sucio.", en="The road is kind of a mess."),
         ]),

    # ---------------------------------------------------------------- place and direction
    dict(w="hacia", pos="prep", grp="Place and direction", tier=2,
         senses=[
             dict(g="towards", ex="El lindero va hacia el río.",
                  en="The boundary runs towards the river."),
         ]),

    dict(w="desde", pos="prep", grp="Place and direction", tier=1,
         senses=[
             dict(g="from (a starting place)", ex="Se ve desde la carretera.",
                  en="You can see it from the road."),
             dict(g="since (a starting time)", ex="Desde marzo estamos esperando.",
                  en="We've been waiting since March."),
         ]),

    dict(w="hasta", pos="prep", grp="Place and direction", tier=1,
         senses=[
             dict(g="until, as far as", ex="El terreno llega hasta el lindero.",
                  en="The land goes as far as the boundary."),
             dict(g="even (emphasis)", ex="Hasta el dueño se sorprendió.",
                  en="Even the owner was surprised."),
         ],
         note="In Mexico and Central America `hasta` often carries a hidden 'not': "
              "`Llega hasta las tres` usually means he doesn't get there until three."),

    dict(w="acá", pos="adv", grp="Place and direction", tier=1,
         senses=[
             dict(g="here, around here", ex="Por acá no hay señal.",
                  en="There's no signal around here."),
         ],
         note="Latin America prefers `acá` and `allá` over `aquí` and `allí`; they are vaguer "
              "about the exact spot, which is usually the point."),

    dict(w="allá", pos="adv", grp="Place and direction", tier=1,
         senses=[
             dict(g="over there", ex="El pozo está allá atrás.",
                  en="The well is back over there."),
         ]),

    # ---------------------------------------------------------------- how people really talk
    dict(w="pues", pos="marker", grp="How people really talk", tier=1,
         senses=[
             dict(g="well, so (buying a moment)", ex="Pues, no sé qué decirte.",
                  en="Well, I don't know what to tell you."),
             dict(g="then (drawing a consequence)",
                  ex="Si no te gusta, pues no lo compres.",
                  en="If you don't like it, then don't buy it."),
         ],
         note="Enormously common and nearly meaningless. Often reduced to `pos` or a single "
              "hissed syllable. Do not go looking for content in it."),

    dict(w="o sea", pos="marker", grp="How people really talk", tier=1,
         senses=[
             dict(g="I mean, that is to say", ex="O sea, no está incluido.",
                  en="I mean, it isn't included."),
         ],
         note="The commonest repair phrase in spoken Spanish. When you hear it, a clarification "
              "is coming -- listen to what follows, not to what you just missed."),

    dict(w="es que", pos="marker", grp="How people really talk", tier=1,
         senses=[
             dict(g="the thing is", ex="Es que no tengo el plano todavía.",
                  en="The thing is, I don't have the survey plan yet."),
         ],
         note="Introduces an explanation, and very often a refusal in polite clothing."),

    dict(w="claro", pos="marker", grp="How people really talk", tier=1,
         senses=[
             dict(g="of course, right", ex="Claro que sí.", en="Of course."),
         ],
         note="`claro que sí` and `claro que no` are emphatic. A bare `claro` is just "
              "'right' -- agreement, not necessarily enthusiasm."),

    dict(w="bueno", pos="marker", grp="How people really talk", tier=1,
         senses=[
             dict(g="right then, OK (taking a turn)",
                  ex="Bueno, entonces firmamos el lunes.",
                  en="Right, so we'll sign on Monday."),
         ],
         note="At the start of a turn it means 'right then', not 'good'. Answering the phone in "
              "Mexico, it means 'hello'."),

    dict(w="igual", pos="adv / adj", grp="How people really talk", tier=1,
         senses=[
             dict(g="anyway, even so", ex="Igual voy a ir.", en="I'm going to go anyway."),
             dict(g="the same", ex="Para mí es igual.", en="It's the same to me."),
         ],
         note="In much of South America a clause-initial `igual` softens to 'anyway' or even "
              "'maybe'. It is not about equality."),

    dict(w="ahorita", pos="adv", grp="How people really talk", tier=1,
         senses=[
             dict(g="in a moment, just now", ex="Ahorita vengo.", en="I'll be right back."),
         ],
         note="Dangerously elastic. In Mexico and Central America it stretches from 'this "
              "second' to 'at some point'. Never hear it as a commitment to a time."),

    dict(w="nomás", pos="adv", grp="How people really talk", tier=2,
         senses=[
             dict(g="just, only", ex="Es nomás una firma.", en="It's just a signature."),
         ]),

    dict(w="de una", pos="marker", grp="How people really talk", tier=2,
         senses=[
             dict(g="right away, let's do it", ex="Vamos de una.", en="Let's go right now."),
         ]),

    dict(w="dale", pos="marker", grp="How people really talk", tier=2,
         senses=[
             dict(g="go on, OK then", ex="Dale, nos vemos el lunes.",
                  en="OK, see you Monday."),
         ]),

    dict(w="fíjate", pos="marker", grp="How people really talk", tier=2,
         senses=[
             dict(g="get this, you see", ex="Fíjate que nunca me llamó.",
                  en="Get this -- he never called me."),
         ],
         note="`fíjate que` nearly always introduces bad news or a complication."),

    dict(w="de repente", pos="adv", grp="How people really talk", tier=2,
         senses=[
             dict(g="suddenly", ex="De repente se levantó y se fue.",
                  en="He suddenly got up and left."),
             dict(g="maybe (Peru and nearby)", ex="De repente mañana firmamos.",
                  en="Maybe we'll sign tomorrow."),
         ],
         note="In Peru this usually means 'maybe'. Taking it as 'suddenly' turns a vague plan "
              "into an event that never happened."),

    dict(w="pendiente", pos="adj", grp="How people really talk", tier=2,
         senses=[
             dict(g="outstanding, still to be done", ex="Está pendiente la firma.",
                  en="The signature is still outstanding."),
             dict(g="keeping an eye on (estar pendiente de)",
                  ex="Estoy pendiente del pago.", en="I'm keeping an eye on the payment."),
         ]),
]


# ---------------------------------------------------------------------------------------------
# Everyday versions of the examples that lean on land, prices and paperwork.
#
# Those examples are right for a learner whose Spanish happens in exactly those conversations,
# and wrong for everyone else: an example's job is to isolate the word being drilled, and a
# sentence carrying `lindero`, `escritura` and `agrimensor` puts three unknowns in front of
# someone who only needed one. 41 of the 90 examples had that problem.
#
# So each of them gets a plain-vocabulary twin, and the reader chooses which set they see. The
# SRS item is the *sense*, not the sentence, so switching sets does not fork anyone's progress.
#
# Keyed by (headword, sense index) -> (spanish, english) or (spanish, english, blank).
PLAIN = {
    ("que", 1): ("La casa que vimos ayer.", "The house we saw yesterday."),
    ("ya", 0): ("Ya comimos.", "We already ate."),
    ("se", 0): ("Aquí se habla español.", "Spanish is spoken here."),
    ("se", 1): ("Se me olvidó el teléfono.", "I forgot my phone."),
    ("se", 3): ("Se lo di a mi hermano.", "I gave it to my brother."),
    ("como", 0): ("Es como mi casa.", "It's like my house."),
    ("mismo", 0): ("Es el mismo día.", "It's the same day."),
    ("algo", 0): ("¿Quieres algo de comer?", "Do you want something to eat?"),
    ("tanto", 1): ("No hay tantos turistas hoy.", "There aren't that many tourists today.", "tantos"),
    ("por", 0): ("Lo hice por ti.", "I did it for you."),
    ("por", 3): ("Escrito por mi hermana.", "Written by my sister."),
    ("para", 2): ("Para entrar necesito la llave.", "To get in, I need the key."),
    ("sino", 0): ("No es café, sino té.", "It isn't coffee, it's tea."),
    ("mientras", 0): ("Mientras comíamos, llamó mi madre.", "While we were eating, my mother called."),
    ("mientras", 1): ("Mientras no llegue, esperamos.", "As long as he doesn't arrive, we'll wait."),
    ("según", 0): ("Según mi hermano, está cerrado.", "According to my brother, it's closed."),
    ("en cuanto", 0): ("En cuanto llegue, te llamo.", "As soon as he arrives, I'll call you."),
    ("ni", 1): ("Ni café ni té, gracias.", "Neither coffee nor tea, thanks."),
    ("además", 0): ("Además, es muy caro.", "Besides, it's very expensive."),
    ("encima", 1): ("Y encima llegó tarde.", "And on top of that, he turned up late."),
    ("ya que", 0): ("Ya que estás aquí, ayúdame.", "Since you're here, give me a hand."),
    ("de todas formas", 0): ("De todas formas hay que ir.", "We have to go anyway."),
    ("cada", 0): ("Cada niño tiene su libro.", "Each child has their own book."),
    ("algún", 0): ("¿Hay algún problema?", "Is there a problem?"),
    ("otro", 0): ("Vimos otro más barato.", "We saw another, cheaper one."),
    ("propio", 0): ("Tiene su propio cuarto.", "She has her own room."),
    ("propio", 1): ("Me lo dijo el propio profesor.", "The teacher himself told me."),
    ("demás", 0): ("Los demás llegan mañana.", "The others arrive tomorrow."),
    ("varios", 0): ("Hay varios restaurantes cerca.", "There are several restaurants nearby."),
    ("medio", 0): ("Media hora.", "Half an hour.", "Media"),
    ("hacia", 0): ("Vamos hacia el centro.", "We're heading towards the centre."),
    ("desde", 0): ("Se ve desde la ventana.", "You can see it from the window."),
    ("hasta", 0): ("El tren llega hasta la playa.", "The train goes as far as the beach."),
    ("hasta", 1): ("Hasta mi hermano vino.", "Even my brother came."),
    ("allá", 0): ("El baño está allá atrás.", "The toilet is back over there."),
    ("es que", 0): ("Es que no tengo tiempo.", "The thing is, I don't have time."),
    ("bueno", 0): ("Bueno, entonces nos vemos el lunes.", "Right, so we'll see each other on Monday."),
    ("nomás", 0): ("Es nomás un minuto.", "It's just a minute."),
    ("de repente", 1): ("De repente vamos mañana.", "Maybe we'll go tomorrow."),
    ("pendiente", 0): ("Está pendiente la respuesta.", "The answer is still outstanding."),
    ("pendiente", 1): ("Estoy pendiente del teléfono.", "I'm keeping an eye on my phone."),
}
