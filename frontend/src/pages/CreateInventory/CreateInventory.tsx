import styles from "./CreateInventory.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { CreateInventory as ICreateInventory } from "../../static/types/Inventory";
import { useReducer, useState } from "react";
import { inventoryStatusNames } from "../../static/types/Status";
import {
  createInventory,
  updateInventoryImage,
} from "../../utils/requests/inventory";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";

function reducer(
  state: ICreateInventory,
  action: { type: keyof ICreateInventory; value: string }
) {
  return {
    ...state,
    [action.type]:
      action.type === "amount" || action.type === "state"
        ? Number(action.value)
        : String(action.value),
  };
}

export function CreateInventory() {
  const [cookies] = useCookies(["SUSI_TOKEN"]);
  const navigate = useNavigate();

  const [state, dispatch] = useReducer(reducer, {
    name: "",
    amount: 1,
    state: 0,
    description: "",
  });

  const [file, setFile] = useState<File>();

  return (
    <Layout>
      <header className={styles.header}>Создать инвентарь</header>
      <input
        type="file"
        accept="image/*"
        onChange={(evt) => {
          setFile(Array.from(evt.target.files ?? [])[0]);
        }}
      />
      <input
        type="text"
        className={styles.input}
        placeholder="Название"
        onChange={(evt) => dispatch({ type: "name", value: evt.target.value })}
      />
      <input
        type="number"
        placeholder="Количество"
        className={styles.input + " " + styles.input_short}
        defaultValue={1}
        onChange={(evt) =>
          dispatch({ type: "amount", value: evt.target.value })
        }
        min={1}
      />
      <select
        className={styles.input}
        defaultValue={0}
        onChange={(evt) => dispatch({ type: "state", value: evt.target.value })}
      >
        {Object.entries(inventoryStatusNames).map((entry, index) => (
          <option value={entry[0]} key={index}>
            {entry[1]}
          </option>
        ))}
      </select>
      <textarea
        className={styles.input + " " + styles.textarea}
        placeholder="Описание"
        onChange={(evt) =>
          dispatch({ type: "description", value: evt.target.value })
        }
      ></textarea>
      <button
        className={styles.btn}
        onClick={() => {
          if (
            state.name !== "" &&
            state.description !== "" &&
            state.amount > 0
          ) {
            createInventory(state)
              .then((inventory) => {
                if (file) {
                  updateInventoryImage(cookies.SUSI_TOKEN, inventory._id, file)
                    .then(() => {
                      navigate("/admin");
                    })
                    .catch((err) => {
                      console.log(err);
                    });
                } else {
                  navigate("/admin");
                }
              })
              .catch((err) => {
                console.log(err);
              });
          }
        }}
      >
        Создать
      </button>
    </Layout>
  );
}
