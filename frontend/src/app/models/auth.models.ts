export interface LoginRequestModel {
    username: string;
    password: string;
}

export interface RegisterRequestModel {
    email: string;
    password: string;
    confirmPassword: string;
}
