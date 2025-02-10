import styles from "./Equipment.module.scss";
import { Inventory } from "../../static/types/Inventory";
import { states } from "../../static/data/states";
import { Link, useNavigate } from "react-router-dom";
import { GetRequestResponse } from "../../static/types/Requests";
import { Status, statusNames } from "../../static/types/Status";
import { deleteInventory } from '../../utils/requests/inventory';

export function Equipment({
  equipment,
  isEditable,
  request,
}: {
  equipment: Inventory;
  isEditable: boolean;
  request?: GetRequestResponse;
}) {
  const navigate = useNavigate();

  return (
    <div className={styles.equipment}>
      {request && request.status !== Status.RETURNED ? (
        <div className={styles.request}>{statusNames[request.status]}</div>
      ) : (
        ""
      )}
      <img
        src={`${import.meta.env.VITE_API_URL}/${equipment.image}`}
        alt=""
        className={styles.image}
      />
      <div className={styles.info}>
        <div className={styles.name}>{equipment.name}</div>
        <div
          className={styles.state}
          style={{ color: states[equipment.state].color }}
        >
          Состояние: {states[equipment.state].text}
        </div>
        <div className={styles.amount}>Количество: {equipment.amount} шт.</div>
        {isEditable ? (
          <div className={styles.btns}>
            <Link to={`/admin/edit/${equipment._id}`} className={styles.btn}>
              Редактировать
            </Link>
            <button className={styles.btn} onClick={() => {
              deleteInventory(equipment._id)
              .then(() => {
                navigate(0);
              })
              .catch(err => {
                console.log(err);
              })
            }}>Удалить</button>
          </div>
        ) : (
          <div className={styles.btns}>
            <Link to={`/get/${equipment._id}`} className={styles.btn}>
              Получить
            </Link>
            <Link to={`/repair/${equipment._id}`} className={styles.btn}>
              Ремонт
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
