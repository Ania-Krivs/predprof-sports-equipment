import styles from "./RepairRequest.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { useReducer, useState, useEffect } from "react";
import { RepairRequestSchema } from "../../static/types/Requests";
import { useParams } from "react-router-dom";
import { getInventoryById } from '../../utils/requests/inventory';
import { Inventory } from '../../static/types/Inventory';

function reducer(
  state: RepairRequestSchema,
  action: { type: keyof RepairRequestSchema; value: string }
) {
  return {
    ...state,
    [action.type]: action.value,
  };
}

export function RepairRequest() {
  const [state, dispatch] = useReducer(reducer, {
    username: "",
    equipment: "",
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
      <header className={styles.header}>Заявка на ремонт инвентаря</header>
      <div className={styles.form}>
        <input
          type="text"
          className={styles.input}
          placeholder="Ваше имя"
          onChange={(evt) =>
            dispatch({ type: "username", value: evt.target.value })
          }
        />
        {
          inventory
          ?
          <div className={styles.input}>{inventory.name}</div>
          :
          ''
        }
        <textarea
          className={styles.input + " " + styles.textarea}
          placeholder="Описание поломки"
          onChange={(evt) =>
            dispatch({ type: "description", value: evt.target.value })
          }
        ></textarea>
        <button className={styles.btn}>Отправить</button>
      </div>
    </Layout>
  );
}
