export type Widget = Readonly<{
  identifier: string;
  title: string;
  value: string;
  kind: 'stat' | 'progress';
  detail: string;
}>;

export type CurrentUser = Readonly<{
  authenticated: boolean;
  display_name: string | null;
  email: string | null;
}>;

async function getJson<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(path, {
    credentials: 'same-origin',
    headers: { Accept: 'application/json' },
    signal,
  });
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const getWidgets = (signal?: AbortSignal): Promise<Widget[]> =>
  getJson<Widget[]>('/api/widgets', signal);

export const getCurrentUser = (signal?: AbortSignal): Promise<CurrentUser> =>
  getJson<CurrentUser>('/auth/me', signal);

export async function logOut(): Promise<void> {
  const response = await fetch('/auth/logout', {
    method: 'POST',
    credentials: 'same-origin',
    headers: { Accept: 'application/json' },
  });
  if (!response.ok) throw new Error('Unable to sign out');
}

