import styles from "./RepairRequest.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { useReducer, useState, useEffect } from "react";
import { RepairRequestSchema } from "../../static/types/Requests";
import { useParams, useNavigate } from "react-router-dom";
import { getInventoryById } from "../../utils/requests/inventory";
import { Inventory } from "../../static/types/Inventory";
import { repairInventoryRequest } from '../../utils/requests/repair';
import { useCookies } from 'react-cookie';

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
  const navigate = useNavigate();
  const [cookies] = useCookies(['SUSI_TOKEN']);

  const [state, dispatch] = useReducer(reducer, {
    inventoryId: "",
    username: "",
    description: "",
  });

  const { id } = useParams();

  const [inventory, setInventory] = useState<Inventory>();

  useEffect(() => {
    getInventoryById(id ?? "")
      .then((inventory) => {
        setInventory(inventory);
        dispatch({type: 'inventoryId', value: inventory._id});
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
        {inventory ? <div className={styles.input}>{inventory.name}</div> : ""}
        <textarea
          className={styles.input + " " + styles.textarea}
          placeholder="Описание поломки"
          onChange={(evt) =>
            dispatch({ type: "description", value: evt.target.value })
          }
        ></textarea>
                <button
          className={styles.btn}
          onClick={() => {
            if (
              inventory &&
              state.username &&
              state.description &&
              state.inventoryId
            ) {
              repairInventoryRequest(cookies.SUSI_TOKEN, state)
                .then(() => {
                  navigate('/');
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
