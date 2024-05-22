package com.ssafy.weSync.record.dto.response;

import com.ssafy.weSync.record.entity.Record;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class GetAllMyResponse {
    private Long recordId;
    private String title;
    private String recordUrl;
    private boolean isPublic;
    private Long startAt;
    private Long endAt;
    private LocalDateTime createdAt;
    private Long teamId;
    private String teamUrl;
    private String songName;
    private String positionName;
    private String colorCode;

    public static GetAllMyResponse toDto(Record record) {
        return builder()
                .recordId(record.getRecordId())
                .title(record.getTitle())
                .recordUrl(record.getUrl())
                .isPublic(record.isPublic())
                .teamId(record.getScore().getTeam().getTeamId())
                .teamUrl(record.getScore().getTeam().getProfileUrl())
                .songName(record.getScore().getTeam().getSongName())
                .positionName(record.getScore().getPosition() != null ? record.getScore().getPosition().getPositionName() : null)
                .colorCode(record.getScore().getPosition() != null && record.getScore().getPosition().getColor() != null
                        ? record.getScore().getPosition().getColor().getColorCode() : null )
                .startAt(record.getStartAt())
                .endAt(record.getEndAt())
                .createdAt(record.getCreatedAt())
                .build();
    }

}