import styles from "./Header.module.scss";
import profileIcon from "../../static/icons/profile.svg";
import exitIcon from "../../static/icons/exit.svg";
import { Link, useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";

export function Header() {
  const navigate = useNavigate();

  const [cookies, , removeCookie] = useCookies(["SUSI_TOKEN"]);

  return (
    <header className={styles.header}>
      <Link to="/" className={styles.logo}>
        СУСИ
      </Link>
      <div className={styles.btns}>
        <button
          className={styles.btn}
          onClick={() => {
            if (!cookies.SUSI_TOKEN) {
              navigate("/login");
            }
          }}
        >
          {cookies.SUSI_TOKEN ? (
            <>
              <span className={styles.text}>adm_1234</span>
              <img src={profileIcon} alt="" className={styles.icon} />
            </>
          ) : (
            "Вход/регистрация"
          )}
        </button>
        {cookies.SUSI_TOKEN ? (
          <button
            className={styles.btn}
            onClick={() => {
              removeCookie("SUSI_TOKEN");
              navigate("/login");
            }}
          >
            <img src={exitIcon} alt="" className={styles.icon} />
          </button>
        ) : (
          ""
        )}
      </div>
    </header>
  );
}
