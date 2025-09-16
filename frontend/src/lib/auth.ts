export function saveToken(token: string) {
  localStorage.setItem("token", token);
}
export function clearToken() {
  localStorage.removeItem("token");
}
export function isAuthed() {
  return !!localStorage.getItem("token");
}
