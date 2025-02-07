import styles from "./Equipment.module.scss";
import { Inventory } from "../../static/types/Inventory";
import { states } from "../../static/data/states";
import { Link } from "react-router-dom";
import { GetRequestResponse } from "../../static/types/Requests";
import { statusNames } from "../../static/types/Status";

export function Equipment({
  equipment,
  isEditable,
  request,
}: {
  equipment: Inventory;
  isEditable: boolean;
  request?: GetRequestResponse;
}) {
  return (
    <div className={styles.equipment}>
      {request ? (
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
