import { Component } from '@angular/core';

@Component({
  selector: 'volontulo-faq-volunteers',
  templateUrl: './faq.component.html',
})
export class FaqVolunteersComponent {
  title = 'wolontariuszy';
  faqs: {
    question: string,
    answer: string,
  }[] = [
    {
      question: `Czym jest wolontariat?`,
      answer: `Nazwa pochodzi od łacińskiego słowa volontarius, które można przetłumaczyć jako “dobrowolny” lub
      “chętny”. Centrum Wolontariatu definiuje wolontariat jako świadomą, dobrowolną działalność podejmowaną na rzecz
      innych, wykraczającą poza więzi rodzinno – przyjacielsko – koleżeńskie. Wolontariuszem jest każda osoba fizyczna,
      która dobrowolnie, ochotniczo i bez wynagrodzenia wykonuje świadczenia na rzecz organizacji, instytucji lub
      osób indywidualnych wykraczając poza więzi koleżeńsko-rodzinne. Zasady wolontariatu zostały opisane w ustawie
      o działalności pożytku publicznego i o wolontariacie uchwalonej w 2003 roku.`
    },
    {
      question: `Kim jest wolontariusz?`,
      answer: `To ludzie, którzy dobrowolnie i bez wynagrodzenia niosą pomoc, angażują się w pracę na rzecz osób i
      instytucji działających w różnych obszarach życia społecznego. Można ich spotkać między innymi w domach dziecka,
      hospicjach, domach pomocy społecznej, muzeach i schroniskach dla zwierząt. Pracują w instytucjach publicznych,
      organizacjach pozarządowych, placówkach kultury, sportu i wielu innych. Wolontariuszem może być każdy, w każdej
      dziedzinie życia społecznego, wszędzie tam, gdzie taka pomoc jest potrzebna. Kandydat na wolontariusza nie musi
      posiadać ściśle kreślonych kompetencji, kwalifikacji (chyba, że organizacja lub instytucja wskazuje na nie
      w ogłoszeniu) - wystarczające są dobre chęci i wolny czas.`,
    },
    {
      question: `Jakie są motywacje, aby stać się wolontariuszem?`,
      answer: `Motywacje, które decydują o zostaniu wolontariuszem to m.in.:
        <ul>
          <li>chęć zrobienia czegoś dobrego, pożytecznego,</li>
          <li>potrzeba kontaktu z ludźmi lub nawiązania nowych znajomości</li>
          <li>chęć bycia potrzebnym</li>
          <li>chęć spłacenia dobra, które kiedyś od kogoś się otrzymało</li>
          <li>chęć zdobycia nowych umiejętności oraz doświadczeń zawodowych i życiowych</li>
        </ul>
        <p>Wolontariat jest także ważny ponieważ:</p>
        <ul>
          <li>uczy wrażliwości na drugiego człowieka,</li>
          <li>pomaga przetrwać okres bezrobocia,</li>
          <li>jest dobrym przygotowaniem do przyszłej pracy</li>
          <li>daje możliwość oderwania się od monotonii codziennego życia.</li>
        </ul>`,
    },
    {
      question: `Czy wolontariuszem może być osoba niepełnoletnia? Czy mój wiek jako wolontariusza jest istotny?`,
      answer: `Wolontariuszem może zostać każdy bez względu na swój wiek. Jednak niektóre formy wolontariatu wymagają
od wolontariusza pełnoletności. Wolontariat jest świadczony na podstawieumowy, którą wolontariusze zawierają z osobą
reprezentującą podmiot, na rzecz którego będą działali. Zasady zawierania umów reguluje Kodeks Cywilny, który bardzo
szczegółowo opisuje, w jaki sposób umowy mogą być zawierane. Osoby niepełnoletnie nie mogą samodzielnie zawrzeć takiej
umowy. W przypadku osoby, która nie ukończyła 13 roku życia, umowę taka może w jej imieniu zawrzeć rodzic lub prawny
opiekun. Jeśli osoba ukończyła 13 rok życia, to umowę taką może zawrzeć samodzielnie, ale tylko za zgodą rodzica lub
prawnego opiekuna – wtedy osoba chcąca zostać wolontariuszem musi przedstawić taką zgodę, najczęściej w formie pisemnej.
 Organizacje chcące korzystać z pracy niepełnoletnich wolontariuszy, aby uniknąć ewentualnych nieprzyjemności, powinny
 prosić kandydatów o przedstawienie pisemnej zgody rodziców.<br />W placówkach opiekuńczo – wychowawczych (zaliczamy
 do nich domy dziecka i świetlice środowiskowe) wolontariuszami mogą być tylko osoby pełnoletnie. W niektórych przypadkach
 wolontariat może być zadaniem bardzo wymagającym, dlatego zgodnie z prawem w niektórych miejscach wolontariusze mogą
 być tylko osoby pełnoletnie. Obecnie takie placówki to: Publiczne poradnie psychologiczno-pedagogiczne w tym publiczne poradnie
 specjalistyczne (podstawa prawna: Rozporządzenie Ministra Edukacji Narodowej z dnia 1 lutego 2013 r. w sprawie szczegółowych zasad
 działania publicznych poradni psychologiczno-pedagogicznych, w tym publicznych  poradni specjalistycznych, Dz. U. nr. 0 poz. 199).`,
    },
    {
      question: `Czy wolontariusz musi posiadać szczególne uprawnienia?`,
      answer: `W zasadzie wolontariuszem może zostać każda osoba bez szczególnych uprawnień. Jednakże, jeżeli wolontariusz
      ma wykonywać świadczenie, dla wykonywania którego przepisy wymagają np. określonych badań, uprawnień etc., to wolontariusz powinien
      takie badania przejść lub też posiadać stosowne uprawnienia. Wymóg ten wynika ze szczególnego charakteru niektórych
      zadań, które mogą być powierzane przez organizację wolontariuszowi, m.in.: w zakresie pomocy społecznej, ochrony zdrowia,
      działania na rzecz osób niepełnosprawnych. Wolontariusz musi posiadać kwalifikacje tylko wtedy, gdy obowiązek ten wynika
      z przepisów prawa.`,
    },
    {
      question: `Ile czasu muszę poświęcić jako wolontariusz?`,
      answer: `Wolontariat może być zajęciem wykonywanym codziennie, jak i raz w tygodniu. Warto się zastanowić, czy ze
      względu na inne obowiązki bardziej odpowiedni dla nas jest wolontariat akcyjny, krótkoterminowy czy długoterminowy.
      To wszystko jest bardzo ważne, ponieważ pozwoli jasno doprecyzować zakres obowiązków danego wolontariusza, a także
      będzie istotną informacją dla organizacji lub instytucji - kiedy można liczyć na pomoc danej osoby. Precyzyjne
      określenie dyspozycyjności przez wolontariusza pozwoli lepiej dopasować jego oczekiwania do potrzeb organizacji
      lub instytucji.`,
    },
    {
      question: `Jakie wolontariusz ma prawa?`,
      answer: `Ustawa o działalności pożytku publicznego i o wolontariacie daje wolontariuszom szereg uprawnień.
Poniżej najważniejsze z nich. Wolontariusz ma prawo do:
        <ul>
          <li>okresu próbnego pozwalającego poznać specyfikę nowej pracy,</li>
          <li>otrzymywania wymaganych środków ochrony osobistej,</li>
          <li>bycia poinformowanym o ryzyku dla zdrowia i bezpieczeństwa związanym z wykonywaniem świadczeń, a
          także o zasadach ochrony przed zagrożeniem,</li>
          <li>zapewnienia, na zasadach takich jak pracownicy, bezpiecznych i higienicznych warunków pracy,</li>
          <li>zwrotu poniesionych kosztów podróży służbowych i diet związanych ze świadczeniem,</li>
          <li>uzyskania pisemnego potwierdzenia treści porozumienia,</li>
          <li>otrzymania zaświadczenia o wykonaniu świadczeń,</li>
          <li>zaopatrzenia z tytułu wykonywania świadczeń – innymi słowy prawo do odszkodowania, a nawet renty
          inwalidzkiej, jeżeli podczas wykonywania świadczeń ulegnie wypadkowi,</li>
          <li>zwrotu pokrycia kosztów ogólnie przyjętych wynikających z umów międzynarodowych, gdy w porozumieniu
          jest mowa o oddelegowaniu wolontariusza na terytorium innego państwa</li>
          <li>bycia poinformowanym o swoich prawach i obowiązkach.</li>
        </ul>`,
    },
    {
      question: `Jakie wolontariusz ma obowiązki?`,
      answer: `Zgodnie z Ustawą o działalności pożytku publicznego i o wolontariacie, wolontariusz powinien posiadać
      kwalifikacje i spełniać wymagania odpowiednie do rodzaju i zakresu świadczonej pomocy, jeżeli taki obowiązek wynika
      z przepisów prawa (np. w przypadku pomocy medycznej osobom bezdomnym lub w przypadku wolontariuszy na stanowisku
      nauczyciela). Jest on również zobligowany do wywiązania się z obowiązków określonych w porozumieniu, nawet jeśli nie
      przybrało ono formy pisemnej. Jest odpowiedzialny również za dbanie o powierzony majątek, mienie rzeczowe, a także
      przestrzegać np. tajemnicy służbowej.`,
    },
    {
      question: `Co to jest etyka pracy wolontariusza?`,
      answer: `Decydując się na działalność w charakterze wolontariusza, należy przestrzegać pewnych zasad. Nie są
one zapisane w żadnych ustawach, kodeksach czy innych przepisach. To nieformalny zbiór norm postępowania, którymi
każdy wolontariusz powinien się kierować. Wśród nich znajdują się takie normy jak m.in.:
        <ul>
          <li>będę wypełniać wszystkie zadania związane z przyjętą rolą;</li>
          <li>nie będę składać obietnic, których nie jestem w stanie spełnić;</li>
          <li>w przypadku niemożności wywiązania się ze zobowiązań, poinformuję o tym koordynatora pracy
          wolontariuszy;</li>
          <li>zachowam dyskrecję w sprawach prywatnych, będę unikać zachowań, które mogą być niewłaściwie
          rozumiane;</li>
          <li>będę otwarty na nowe pomysły i sposoby działania;</li>
          <li>wykorzystam szansę poznania i nauczenia się nowych rzeczy od innych osób;</li>
          <li>nie będę krytykować rzeczy, których nie rozumiem;</li>
          <li>będę pytać o rzeczy, których nie rozumiem;</li>
          <li>będę działać w zespole;</li>
          <li>będę osobą, na której można polegać;</li>
          <li>będę pracować lepiej i z większą satysfakcją wykonując to, czego się ode mnie oczekuje;</li>
          <li>będę chętnie się uczyć; wiem, że nauka jest nieodłączną częścią każdej dobrze wykonanej pracy;</li>
          <li>będę uczestniczyć w obowiązkowych spotkaniach;</li>
          <li>postaram się być bardzo dobrym wolontariuszem.</li>
        </ul>`,
    },
    {
      question: `Gdzie wolontariusz może pomagać?`,
      answer: `Wolontariuszem można być wszędzie z wyłączeniem sektora biznesu. Miejsca, w których można świadczyć pracę
      wolontarystyczną to m.in.: stowarzyszenia, fundacje, instytucje, które są organami administracji publicznej
      (ministerstwa, urzędy miejskie), wszystkie jednostki organizacyjne, które podlegają organom administracji publicznej
      (m.in. ośrodki pomocy społecznej, biblioteki, muzea, szkoły, uczelnie, przedszkola, szpitale publiczne. Inne miejsca,
      które mogą angażować wolontariuszy to choćby organizacje kościelne, stowarzyszenia jednostek samorządu terytorialnego,
      organizacje pracodawców, kluby sportowe i policja. Jeżeli natomiast kogoś interesuje pomoc osobom fizycznym –
      indywidualnym (np. wielodzietnej rodzinie z bloku obok czy dziecku ze szkoły osiedlowej, które ma kłopoty w nauce),
      tu sprawa wygląda nieco inaczej. Można to oczywiście zrobić, ale musimy pamiętać o jednym: osoba indywidualna nie ma
      takich uprawnień jak organizacje bądź instytucje, nie może podpisać z nami porozumienia o współpracy, a więc nie może
      samodzielnie skorzystać z pomocy wolontariusza. Może to zrobić tylko za pośrednictwem wyżej wymienionych placówek.`,
    },
    {
      question: `Czy wolontariusz dostaje wynagrodzenie?`,
      answer: `Wolontariusz wykonuje świadczenia na rzecz korzystającego ochotniczo i bez wynagrodzenia. Z powyższego wynika, że
      wolontariusz za wykonywane przez siebie świadczenia nie może otrzymywać wynagrodzenia.`,
    },
    {
      question: `Czym się różni wolontariat zagraniczny od krajowego?`,
      answer: `Staże i wolontariaty odbywane za granicą różnią się od tych realizowanych w miejscu zamieszkania przede
      wszystkim kosztami. Na całym świecie organizacje przyjmujące wolontariuszy nie płacą im za ich pracę i zaangażowanie,
      nie opłacają też ich przyjazdu, zakwaterowania, wyżywienia i ubezpieczenia. Wszystkie koszty ponosi sam wolontariusz.`,
    },
    {
      question: `Czy można być wolontariuszem za granicą?`,
      answer: `Tak. Osoba, która chce zostać wolontariuszem za granicą musi być pełnoletnia i znać język angielski lub język kraju,
      do którego zamierza się wybrać. Najczęściej poszukiwane są osoby mające już jakiekolwiek doświadczenie wolontarystyczne, ale nie
      jest to obowiązek. Jeśli wolontariusz udaje się do egotycznych krajów (np. w Afryce, Azji, czy Ameryce Południowej), powinien
      zainteresować się, czy nie musi poddać się odpowiednim szczepieniom. Polecamy zasięgnąć opinii i wiedzy u organizacji zajmujących
      się wolontariatem za granicą.`,
    },
    {
      question: `Czy cudzoziemcy mogą być wolontariuszami?`,
      answer: `Wolontariuszami mogą być nie tylko obywatele polscy, ale także cudzoziemcy legalnie przebywający w Polsce.
      Zgodnie z art. 42 ust.1 świadczenie wolontariuszy jest świadczeniem odpowiadającym świadczeniu pracy, nie jest natomiast
      świadczeniem pracy lub usług. W związku z tym wolontariusz – cudzoziemiec nie musi uzyskiwać zezwolenia na pracę aby
      zostać wolontariuszem.`,
    },
    {
      question: `Czy mogę zamienić praktyki studenckie czy staż na wolontariat?`,
      answer: `Wolontariatem nie są praktyki studenckie ani staż. Praktyki studenckie są formą zdobywania praktycznej wiedzy
      związanej z kierunkiem studiów. Ich odbycie jest obowiązkiem studenta wynikającym np. z regulaminu uczelni, a więc
      praktyka studencka, choć bezpłatna - nie jest dobrowolna i nie jest wolontariatem. A wolontariusz to osoba, która
      ochotniczo i bez wynagrodzenia wykonuje świadczenia odpowiadające świadczeniom pracy, wykraczając poza obszar swoich
      codziennych obowiązków.`,
    },
    {
      question: `Czy okres pracy wolontarystycznej liczy się do stażu pracy?`,
      answer: `Nie. Tak samo wykonywanie świadczeń przez wolontariusza nie wpływa na uprawnienia pracownicze. Nie można więc
      okresu pracy wolontariusza wliczyć do okresów składkowych lub nieskładkowych, co w efekcie nie ma wpływu na uzyskanie
      prawa do renty, czy emerytury ani tym bardziej na wysokość obu tych świadczeń.`,
    },
    {
      question: `Czy wolontariusz jest pracownikiem?`,
      answer: `Nie. Świadczenie wykonywane przez wolontariusza jest „świadczeniem odpowiadającym świadczeniu pracy”,
nie jest to praca w rozumieniu Kodeksu Pracy. Są jeszcze dwie istotne różnice:
        <ul>
          <li>wolontariusz za swoją pracę nie pobiera wynagrodzenia;</li>
          <li>wolontariusz podpisuje porozumienie o współpracy, a nie umowę o pracę.</li>
        </ul>`,
    },
    {
      question: `Czy osoba bezrobotna może być wolontariuszem bez utraty prawa do zasiłku?`,
      answer: `			Tak. Bycie wolontariuszem nie wpływa ani na utratę, ani na wysokość świadczenia dla bezrobotnych.
      Wolontariusz nie jest pracownikiem w rozumieniu Kodeksu Pracy, a&nbsp;więc nie straci prawa do zasiłku.`,
    },
    {
      question: `Czy podmioty gospodarcze mogą korzystać z pomocy wolontariuszy?`,
      answer: `Ustawa nie przewiduje możliwości angażowania wolontariuszy przez podmioty gospodarcze. Ze względu na cel
      i charakter świadczeń wolontariuszy nie jest dopuszczalne, aby wykonywali oni świadczenia na rzecz przedsiębiorców i
      innych podmiotów prowadzących działalność gospodarczą. Wolontariusze nie powinni również zastępować pracowników a jedynie
      uzupełniać ich pracę. Oznacza to, że w żadnej sytuacji firmy, sklepy, kancelarie prawne czy biura rachunkowe nie mogą
      korzystać z pomocy wolontariuszy. Nawet, gdy podejmują działania prospołeczne.`,
    },
    {
      question: `Czy wolontariusz musi mieć podpisane porozumienie?`,
      answer: `Wolontariusz pracuje w organizacji na podstawie i w oparciu o porozumienie zawarte z organizacją. W przypadku
      wolontariatu przekraczającego 30 dni porozumienie musi mieć formę pisemną. Dla porozumień obejmujących wolontariat krótkoterminowy
      (poniżej 30 dni) wystarczy forma ustna. Jednakże zawsze na żądania wolontariusza porozumienie musi zostać zawarte na piśmie.`,
    },
    {
      question: `Co powinno zawierać porozumienie?`,
      answer: `Porozumienie powinno zawierać zakres, sposób i czas wykonywania świadczenia, a także postanowienie o możliwości jego
      rozwiązania.`,
    },
    {
      question: `Czy wolontariusz w trakcie lub po zakończeniu świadczenia może zażądać wydania pisemnego zaświadczenia?`,
      answer: `Tak. Takie zaświadczenie powinno zawierać informację o tym, co wolontariusz robił w ramach swoich obowiązków oraz
      jakie zdobył doświadczenie. Organizacja ma obowiązek wystawić zaświadczenie na każdą prośbę wolontariusza.`,
    },
    {
      question: `Czy organizacja ma obowiązek pokrywania kosztów podróży służbowych i diet wolontariusza?`,
      answer: `Tak, organizacja ma obowiązek pokrywania kosztów podróży służbowych i diet wolontariusza a zasadach dotyczących
      pracowników. Jednakże wolontariusz może się zrzec tego uprawnienia podpisując odpowiednie oświadczenie.`,
    },
    {
      question: `Kiedy wolontariuszowi przysługuje ubezpieczenie od Następstw Nieszczęśliwych Wypadków?`,
      answer: `Ubezpieczenie NNW organizacja zobowiązana jest pokrywać w razie zawarcia umowy na czas krótszy niż 30 dni. W tym
wypadku organizacja musi wykupić dla swoich wolontariuszy ubezpieczenie NW. Jeżeli natomiast organizacja zawiera porozumienie na
czas dłuższy niż 30 dni i na czas określony to wolontariusz zostaje objęty ubezpieczeniem na mocy tzw. małej ustawy wypadkowej.
<br />W wypadku zawarcia umowy z wolontariuszem na czas nieokreślony organizacja musi wykupić mu ubezpieczenie NW przez pierwszych
30 dni. Od początku drugiego miesiąca wykonywania świadczeń przez wolontariusza zostaje on objęty ubezpieczeniem na mocy małej
ustawy wypadkowej.`,
    },
    {
      question: `Czy świadczenia wolontarystyczne mogą być traktowane jako darowizna?`,
      answer: `Nie. Świadczenia wolontarystyczne nie mogą być traktowane jako darowizna.`,
    },
    {
      question: `Czy członek/członkini stowarzyszenia może być wolontariuszem w swojej organizacji?`,
      answer: `Tak. 12 marca 2010 roku weszły w życie zmiany w dotychczasowej ustawie o działalności pożytku publicznego i wolontariacie.
      Jedna z nich mówi, że członek lub członkini swojej organizacji może być w niej jednocześnie wolontariuszem.`,
    },
    {
      question: `Czy organizacja ma obowiązek wysyłania wolontariusza na dodatkowe szkolenia z zakresu działalności, jakiej się podejmuje
      jako wolontariusz?`,
      answer: `Nie. Jednakże jeżeli organizacja uzna, że ma na takie szkolenie środki i uważa udział w szkoleniu za zasadny, to może
      zapewnić wolontariuszowi udział w interesujących szkoleniach.`,
    },
    {
      question: `Czy Szkolny Klub Wolontariusza musi być gdzieś zarejestrowany?`,
      answer: `Nie.`,
    },
    {
      question: `Czy w organizacji przyjmującej wolontariuszy musi być koordynator pracy wolontariuszy?`,
      answer: `Nie jest to obowiązek prawny. Natomiast doświadczenie podpowiada, że w organizacji powinna być wyznaczona osoba,
      która będzie koordynowała pracę wolontariuszy, przeprowadzała wstępną rozmowę, wprowadzi wolontariuszy w życie organizacji,
      wskaże zakres zadań, dba o relacje z wolontariuszami oraz o jakość świadczeń.`,
    },
    {
      question: `Jak można nagradzać swoich wolontariuszy?`,
      answer: `Wiele form i możliwości nagradzania swoich wolontariuszy. W zależności od zasobów i środków, którymi dysponujemy,
      mogą być to np.: listy gratulacyjne, dyplomy, zaproszenia na dodatkowe warsztaty, zaproszenia na spotkania zespołu pracowników,
      informacja na stronie internetowej, pochwała przed innymi wolontariuszami, powierzanie coraz bardziej odpowiedzialnych zadań,
      wdrażanie pomysłów wolontariuszy, wpis do księgi pamiątkowej, impreza z okazji Dnia Wolontariusza, wysyłanie kartek
      okolicznościowych, drobne gadżety, własne stanowisko pracy itd.`,
    },
  ];
}
