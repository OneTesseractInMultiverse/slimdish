import {
  Button,
  Column,
  Grid,
  Header,
  HeaderGlobalAction,
  HeaderGlobalBar,
  HeaderName,
  InlineLoading,
  InlineNotification,
} from '@carbon/react';
import { Login, Logout } from '@carbon/icons-react';
import { useEffect, useState } from 'react';
import { WidgetCard } from './components/WidgetCard';
import { getCurrentUser, getWidgets, logOut, type CurrentUser, type Widget } from './services/dashboard';

export default function App() {
  const [widgets, setWidgets] = useState<Widget[]>([]);
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    Promise.all([getWidgets(controller.signal), getCurrentUser(controller.signal)])
      .then(([loadedWidgets, loadedUser]) => {
        setWidgets(loadedWidgets);
        setUser(loadedUser);
      })
      .catch((reason: unknown) => {
        if (!(reason instanceof DOMException && reason.name === 'AbortError')) {
          setError('The dashboard could not be loaded. Please try again.');
        }
      });
    return () => controller.abort();
  }, []);

  const handleLogout = async () => {
    await logOut();
    window.location.reload();
  };

  return (
    <>
      <Header aria-label="SlimDash">
        <HeaderName href="/" prefix="Slim">Dash</HeaderName>
        <HeaderGlobalBar>
          {user?.authenticated ? (
            <HeaderGlobalAction aria-label="Sign out" onClick={() => void handleLogout()}>
              <Logout />
            </HeaderGlobalAction>
          ) : (
            <HeaderGlobalAction aria-label="Sign in with W3ID" onClick={() => { window.location.href = '/auth/login'; }}>
              <Login />
            </HeaderGlobalAction>
          )}
        </HeaderGlobalBar>
      </Header>
      <main className="dashboard">
        <Grid>
          <Column sm={4} md={8} lg={16}>
            <p className="dashboard__eyebrow">Overview</p>
            <h1>Good to see you{user?.authenticated ? `, ${user.display_name}` : ''}.</h1>
            <p className="dashboard__intro">A focused view of the work that needs your attention.</p>
          </Column>
          {error && (
            <Column sm={4} md={8} lg={16}>
              <InlineNotification kind="error" title="Unable to load" subtitle={error} hideCloseButton />
            </Column>
          )}
          {!error && widgets.length === 0 && (
            <Column sm={4} md={8} lg={16}><InlineLoading description="Loading dashboard" /></Column>
          )}
          {widgets.map((widget) => (
            <Column key={widget.identifier} sm={4} md={4} lg={8}>
              <WidgetCard widget={widget} />
            </Column>
          ))}
          {!user?.authenticated && user !== null && (
            <Column sm={4} md={8} lg={16} className="dashboard__signin">
              <Button href="/auth/login" renderIcon={Login}>Sign in with W3ID</Button>
            </Column>
          )}
        </Grid>
      </main>
    </>
  );
}

