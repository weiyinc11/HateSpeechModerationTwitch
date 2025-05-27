export interface GenerateOptions {
	length?: number;
	readable?: boolean;
	charset?: string;
	capitalization?: string;
}

declare function generate(options?: GenerateOptions | number): string;

export { generate };
export default generate;
