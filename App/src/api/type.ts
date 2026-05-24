export interface OcrResult {
    bank: string;
    amount: string;
}

export interface ApiResponse {
    result: OcrResult;
}