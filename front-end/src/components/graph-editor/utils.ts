
// Gerar nome automático para vértice com letras minúsculas
export const generateNodeName = (usedNames: Set<string>): string => {
  const getLetterName = (num: number): string => {
    let name = '';
    let n = num;
    
    if (n < 26) {
      // a-z
      return String.fromCharCode(97 + n);
    } else {
      // aa, ab, ac, ... 
      const firstLetter = Math.floor((n - 26) / 26);
      const secondLetter = (n - 26) % 26;
      return String.fromCharCode(97 + firstLetter) + String.fromCharCode(97 + secondLetter);
    }
  };
  
  let index = 0;
  let name = getLetterName(index);
  
  // Encontrar próximo nome disponível
  while (usedNames.has(name)) {
    index++;
    name = getLetterName(index);
  }
  
  return name;
};
