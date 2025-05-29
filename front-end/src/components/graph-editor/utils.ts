export const generateNodeName = (usedNames: Set<string>): string => {
  const getLetterName = (num: number): string => {
    let name = '';
    let n = num;
    if (n < 26) return String.fromCharCode(97 + n);
    const firstLetter = Math.floor((n - 26) / 26);
    const secondLetter = (n - 26) % 26;
    return String.fromCharCode(97 + firstLetter) + String.fromCharCode(97 + secondLetter);
  };
  let index = 0;
  let name = getLetterName(index);
  while (usedNames.has(name)) {
    index++;
    name = getLetterName(index);
  }
  return name;
};
