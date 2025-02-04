import styles from './Layout.module.scss';
import { ReactNode, useEffect } from 'react';
import { Header } from '../Header/Header';
import { useNavigate } from 'react-router-dom';
import { useCookies } from 'react-cookie';

export function Layout({children}: {children: ReactNode}) {
  const navigate = useNavigate();

  const [cookies] = useCookies(['SUSI_TOKEN']);

  useEffect(() => {
    if (!cookies.SUSI_TOKEN) {
      navigate('/login');
    }
  }, []);

  return (
    <div className={styles.wrapper}>
      <Header />
      <main className={styles.main}>
        {children}
      </main>
    </div>
  )
}