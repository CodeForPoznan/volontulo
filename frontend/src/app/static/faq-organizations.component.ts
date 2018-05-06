import { Component } from '@angular/core';

@Component({
  selector: 'volontulo-faq-organizations',
  templateUrl: './faq.component.html',
})

export class FaqOrganizationsComponent {
  title = 'organizatorów';
  faqs: {
    question: string,
    answer: string,
  }[] = [
    {
      question: `Czy wolontariuszem może być osoba niepełnoletnia?`,
      answer: `W przypadku osób, które nie są pełnoletnie na rozpoczęcie działalności woluntarystycznej wymagana jest zgoda przedstawiciela
      ustawowego (zazwyczaj – rodziców). Organizacje chcące korzystać z pracy niepełnoletnich wolontariuszy, aby uniknąć ewentualnych
      nieprzyjemności powinny prosić kandydatów o przedstawienie pisemnej zgody rodziców. W placówkach opiekuńczo – wychowawczych
      (zaliczamy do nich domy dziecka i świetlice środowiskowe), wolontariuszami mogą być tylko osoby pełnoletnie.`,
    },
    {
      question: `Na rzecz jakich podmiotów wolontariusze mogą wykonywać świadczenia?`,
      answer: `Ustawa o działalności pożytku publicznego i o wolontariacie w art. 42 ust. 1 określa krąg podmiotów uprawnionych do
zawierania porozumień z wolontariuszami, zwanych w ustawie korzystającymi. Są nimi:
        <ul>
          <li>organizacje pozarządowe oraz inne podmioty prowadzące działalność pożytku publicznego – w zakresie ich działalności
          statutowej (a nie gospodarczej), w szczególności w zakresie działalności pożytku publicznego,</li>
          <li>jednostki organizacyjne podległe organom administracji publicznej lub nadzorowane przez te organy – z wyłączeniem
          prowadzonej przez te jednostki działalności gospodarczej,</li>
          <li>organy administracji publicznej – z wyłączeniem prowadzadzonej przez nie działalności gospodarczej.</li>
        </ul>`,
    },
    {
      question: `Czy wolontariusz może działać na rzecz przedsiębiorców?`,
      answer: `Podmioty, na rzecz których wolontariusz może wykonywać świadczenia zostały określone powyżej. Ponadto, ze względu na cel
      i charakter świadczeń wolontariuszy nie jest dopuszczalne, aby wykonywali oni świadczenia na rzecz przedsiębiorców i innych
      podmiotów prowadzących działalność gospodarczą. Wolontariusze nie powinni również zastępować pracowników a jedynie uzupełniać
      ich pracę.`,
    },
    {
      question: `Czy wolontariusz jest pracownikiem?`,
      answer: `Wolontariusz nie jest pracownikiem, ponieważ, za wykonanie świadczenia na rzecz korzystającego, wolontariusz nie pobiera
      wynagrodzenia i wykonuje je na podstawie porozumienia, a nie umowy o pracę (art.3 w zw. z art.42 ustawy). Ponadto wykonywane przez
      wolontariusza świadczenie nie jest świadczeniem pracy, lecz świadczeniem odpowiadającym świadczeniu pracy.`
    },
    {
      question: `Czy wolontariusz musi mieć podpisane porozumienie?`,
      answer: `Wolontariusz pracuje w organizacji na podstawie i w oparciu o porozumienie zawarte z organizacją. W przypadku wolontariatu
      przekraczającego 30 dni porozumienie musi mieć formę pisemną. Dla porozumień obejmujących wolontariat krótkoterminowy (poniżej 30
      dni) wystarczy forma ustna. Jednakże zawsze na żądania wolontariusza porozumienie musi zostać zawarte na piśmie. Porozumienie
      powinno zawierać zakres, sposób i czas wykonywania świadczenia, a także postanowienie o możliwości jego rozwiązania.`,
    },
    {
      question: `Jakie obowiązki będą spoczywały na podmiotach uprawnionych do zawierania z wolontariuszami porozumień?`,
      answer: `Z art. 45 ustawy wynika, że korzystający jest zobowiązany do zapewnienia odpowiednich środków ochrony indywidualnej
      uzależnionych od rodzaju świadczeń i zagrożeń związanych z ich wykonywaniem. Korzystający ma również obowiązek informowania
      wolontariusza o ryzyku dla zdrowia i bezpieczeństwa związanym z wykonywanymi świadczeniami oraz o zasadach ochrony przed
      zagrożeniami, jak również do zapewnienia wolontariuszom bezpiecznych i higienicznych warunków wykonywania świadczeń.`,
    },
    {
      question: `Czy członek/członkini stowarzyszenia może być wolontariuszem w swojej organizacji?`,
      answer: `Tak. 12 marca 2010 roku weszły w życie zmiany w dotychczasowej ustawie o działalności pożytku publicznego i wolontariacie.
      Jedna z nich mówi, że członek lub członkini swojej organizacji może być w niej jednocześnie wolontariuszem.`,
    },
    {
      question: `Czy Szkolny Klub Wolontariusza musi być gdzieś zarejestrowany?`,
      answer: `Nie`,
    },
    {
      question: `Jak można nagradzać swoich wolontariuszy?`,
      answer: `Jest wiele form i możliwości nagradzania swoich wolontariuszy. W zależności od zasobów i środków, którymi dysponujemy,
      mogą być to np.: listy gratulacyjne, dyplomy, zaproszenia na dodatkowe warsztaty, zaproszenia na spotkania zespołu pracowników,
      informacja na stronie internetowej, pochwała przed innymi wolontariuszami, powierzanie coraz bardziej odpowiedzialnych zadań,
      wdrażanie pomysłów wolontariuszy, wpis do księgi pamiątkowej, impreza z okazji Dnia Wolontariusza, wysyłanie kartek
      okolicznościowych, drobne gadżety, własne stanowisko pracy itd.`,
    },
  ];
}
