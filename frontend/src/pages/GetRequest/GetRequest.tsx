import styles from "./GetRequest.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { useEffect, useReducer, useState } from "react";
import { GetRequestSchema } from "../../static/types/Requests";
import { useParams } from "react-router-dom";
import { Inventory } from "../../static/types/Inventory";
import { getInventoryById } from "../../utils/requests/inventory";

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
  const [state, dispatch] = useReducer(reducer, {
    username: "",
    equipment: "",
    amount: 0,
    description: "",
  });

  const { id } = useParams();

  const [inventory, setInventory] = useState<Inventory>();

  useEffect(() => {
    getInventoryById(id ?? "")
      .then((inventory) => {
        setInventory(inventory);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <Layout>
      <header className={styles.header}>Заявка на получение инвентаря</header>
      <div className={styles.form}>
        <input
          type="text"
          className={styles.input}
          placeholder="Ваше имя"
          onChange={(evt) =>
            dispatch({ type: "username", value: evt.target.value })
          }
        />
        {inventory ? <div className={styles.input}>{inventory.name}</div> : ""}
        <input
          type="number"
          placeholder="Количество"
          className={styles.input + " " + styles.input_short}
          defaultValue={0}
          onChange={(evt) =>
            dispatch({ type: "amount", value: evt.target.value })
          }
        />
        <textarea
          className={styles.input + " " + styles.textarea}
          placeholder="Цель использования"
          onChange={(evt) =>
            dispatch({ type: "description", value: evt.target.value })
          }
        ></textarea>
        <button className={styles.btn}>Отправить</button>
      </div>
    </Layout>
  );
}
