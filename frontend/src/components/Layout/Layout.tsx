import styles from './Layout.module.scss';
import { ReactNode } from 'react';
import { Header } from '../Header/Header';

export function Layout({children}: {children: ReactNode}) {
  return (
    <div className={styles.wrapper}>
      <Header />
      <main className={styles.main}>
        {children}
      </main>
    </div>
  )
}