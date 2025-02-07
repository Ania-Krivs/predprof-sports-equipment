import styles from "./GetRequest.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { useEffect, useReducer, useState } from "react";
import { GetRequestSchema } from "../../static/types/Requests";
import { useNavigate, useParams } from "react-router-dom";
import { Inventory } from "../../static/types/Inventory";
import { getInventoryById } from "../../utils/requests/inventory";
import { invokeGetInventoryRequest } from "../../utils/requests/get";
import { useCookies } from "react-cookie";
import { getUser } from "../../utils/requests/user";
import { User } from "../../static/types/User";

function reducer(
  state: GetRequestSchema,
  action: { type: keyof GetRequestSchema; value: string }
) {
  return {
    ...state,
    [action.type]:
      action.type === "amount" ? Number(action.value) : String(action.value),
  };
}

export function GetRequest() {
  const navigate = useNavigate();
  const [cookies] = useCookies(["SUSI_TOKEN"]);

  const [state, dispatch] = useReducer(reducer, {
    inventoryId: "",
    description: "",
    amount: 1,
  });

  const { id } = useParams();

  const [inventory, setInventory] = useState<Inventory>();
  const [user, setUser] = useState<User>();

  useEffect(() => {
    getInventoryById(id ?? "")
      .then((inventory) => {
        setInventory(inventory);
        dispatch({ type: "inventoryId", value: inventory._id });
      })
      .catch((err) => {
        console.log(err);
      });
    getUser(cookies.SUSI_TOKEN)
      .then((user) => {
        setUser(user);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <Layout>
      <header className={styles.header}>Заявка на получение инвентаря</header>
      <div className={styles.form}>
        {user ? <div className={styles.input}>{user.username}</div> : ""}
        {inventory ? <div className={styles.input}>{inventory.name}</div> : ""}
        {inventory ? (
          <input
            type="number"
            placeholder="Количество"
            className={styles.input + " " + styles.input_short}
            defaultValue={1}
            onChange={(evt) =>
              dispatch({ type: "amount", value: evt.target.value })
            }
            min={1}
            max={inventory.amount}
          />
        ) : (
          ""
        )}
        <textarea
          className={styles.input + " " + styles.textarea}
          placeholder="Цель использования"
          onChange={(evt) =>
            dispatch({ type: "description", value: evt.target.value })
          }
        ></textarea>
        <button
          className={styles.btn}
          onClick={() => {
            if (
              user &&
              inventory &&
              state.amount > 0 &&
              state.amount <= inventory.amount &&
              state.description &&
              state.inventoryId
            ) {
              invokeGetInventoryRequest(cookies.SUSI_TOKEN, state)
                .then(() => {
                  navigate("/");
                })
                .catch((err) => {
                  console.log(err);
                });
            }
          }}
        >
          Отправить
        </button>
      </div>
    </Layout>
  );
}
