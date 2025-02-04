import styles from "./Header.module.scss";
import profileIcon from "../../static/icons/profile.svg";
import exitIcon from "../../static/icons/exit.svg";
import { Link, useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import { useEffect, useState } from "react";
import { User } from "../../static/types/User";
import { getUser } from "../../utils/requests/user";

export function Header() {
  const navigate = useNavigate();

  const [cookies, , removeCookie] = useCookies(["SUSI_TOKEN"]);

  const [user, setUser] = useState<User>();

  useEffect(() => {
    getUser(cookies.SUSI_TOKEN)
      .then((user) => {
        setUser(user);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

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
          {cookies.SUSI_TOKEN && user ? (
            <>
              <span className={styles.text}>{user.username}</span>
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
              removeCookie("SUSI_TOKEN", {
                path: "/",
              });
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
