import randomstring from './lib/randomstring.js';

const { generate: generateRandomString } = randomstring;

export default generateRandomString;
export { generateRandomString as generate };
