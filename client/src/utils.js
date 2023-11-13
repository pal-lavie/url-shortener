import dayjs from "dayjs";

export const formatDate = (date) => dayjs(date).format('YYYY MMM DD, HH:mm A');
