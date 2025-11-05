export function isParsed(str) {
  let i = 0;
  
  function S() {
    if (i < str.length && str[i] === "(") {
      i++;
      if (!S()) return false;
      if (i < str.length && str[i] === ")") {
        i++;
        return true;
      }
      return false;
    }
    return true;
  }
  
  return S() && i === str.length;
}
