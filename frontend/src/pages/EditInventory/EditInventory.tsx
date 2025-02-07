import styles from "./EditInventory.module.scss";
import { Layout } from "../../components/Layout/Layout";
import {
  EditInventory as IEditInventory,
  Inventory,
} from "../../static/types/Inventory";
import { useEffect, useReducer, useState } from "react";
import { inventoryStatusNames } from "../../static/types/Status";
import {
  editInventory,
  getInventoryById,
} from "../../utils/requests/inventory";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";

function reducer(
  state: IEditInventory,
  action: { type: keyof IEditInventory; value: string }
) {
  return {
    ...state,
    [action.type]:
      action.type === "amount" || action.type === "state"
        ? Number(action.value)
        : String(action.value),
  };
}

export function EditInventory() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [state, dispatch] = useReducer(reducer, {
    id: "",
    name: "",
    amount: 0,
    state: 0,
    description: "",
  });

  const [inventory, setInventory] = useState<Inventory>();

  useEffect(() => {
    if (id) {
      getInventoryById(id)
        .then((inventory) => {
          setInventory(inventory);
          dispatch({ type: "id", value: inventory._id });
          dispatch({ type: "name", value: inventory.name });
          dispatch({ type: "amount", value: String(inventory.amount) });
          dispatch({ type: "description", value: inventory.description });
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, []);

  return (
    <Layout>
      <header className={styles.header}>Редактировать инвентарь</header>
      {inventory ? (
        <>
          <input
            type="text"
            className={styles.input}
            placeholder="Название"
            onChange={(evt) =>
              dispatch({ type: "name", value: evt.target.value })
            }
            defaultValue={inventory.name}
          />
          <input
            type="number"
            placeholder="Количество"
            className={styles.input + " " + styles.input_short}
            onChange={(evt) =>
              dispatch({ type: "amount", value: evt.target.value })
            }
            min={1}
            defaultValue={Number(inventory.amount)}
          />
          <select
            className={styles.input}
            onChange={(evt) =>
              dispatch({ type: "state", value: evt.target.value })
            }
            defaultValue={inventory.state}
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
            defaultValue={inventory.description}
          ></textarea>
          <button
            className={styles.btn}
            onClick={() => {
              if (
                state.name !== "" &&
                state.description !== "" &&
                state.amount > 0
              ) {
                editInventory(state)
                  .then(() => {
                    navigate("/admin");
                  })
                  .catch((err) => {
                    console.log(err);
                  });
              }
            }}
          >
            Сохранить
          </button>
        </>
      ) : (
        ""
      )}
    </Layout>
  );
}
