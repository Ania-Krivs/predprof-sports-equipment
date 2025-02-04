import styles from "./Login.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { useState } from "react";
import { loginUser, registerUser } from "../../utils/requests/user";
import { useNavigate } from "react-router-dom";
import { useCookies } from 'react-cookie';

export function Login() {
  const navigate = useNavigate();
  const [, setCookie] = useCookies(["SUSI_TOKEN"]);

  const [regMode, setRegMode] = useState<boolean>(false);

  const [login, setLogin] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  return (
    <Layout>
      <div className={styles.form}>
        <header className={styles.header}>
          {regMode ? "Регистрация" : "Вход"}
        </header>
        <input
          type="text"
          className={styles.input}
          placeholder="Введите логин"
          onChange={(evt) => setLogin(evt.target.value)}
        />
        <input
          type="password"
          className={styles.input}
          placeholder="Введите пароль"
          onChange={(evt) => setPassword(evt.target.value)}
        />
        <div className={styles.btns}>
          <button
            className={styles.btn}
            onClick={() => {
              if (regMode) {
                registerUser(login, password)
                  .then((token) => {
                    setCookie('SUSI_TOKEN', token.user_token);
                    navigate('/');
                  })
                  .catch((err) => {
                    console.log(err);
                  });
              } else {
                loginUser(login, password)
                  .then((token) => {
                    setCookie('SUSI_TOKEN', token.user_token);
                    navigate('/');
                  })
                  .catch((err) => {
                    console.log(err);
                  });
              }
            }}
          >
            {regMode ? "Зарегистрироваться" : "Войти"}
          </button>
          <button
            className={styles.btn}
            onClick={() => setRegMode((regMode) => !regMode)}
          >
            {regMode ? "Вход" : "Регистрация"}
          </button>
        </div>
      </div>
    </Layout>
  );
}
